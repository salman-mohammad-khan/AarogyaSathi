#!/usr/bin/env bash
# Deploy the current git commit to the VM: test, back up, upload, restart, health check, auto-rollback.
#
# Usage:   DEPLOY_HOST=ubuntu@<vm-ip> scripts/deploy.sh [--dry-run]
# Options (environment variables):
#   DEPLOY_HOST    required, e.g. ubuntu@203.0.113.10 (not stored in the repo on purpose)
#   DEPLOY_KEY     SSH private key, default ~/.ssh/id_ed25519
#   APP_DIR        app folder on the VM, default /opt/healthbot
#   SERVICE        systemd unit name, default healthbot
#   BACKUP_DIR     where backups are written on the VM, default /opt/healthbot-backups
#   HEALTH_TIMEOUT seconds to wait for the service after restart, default 240 (the model reload is slow)
#   SKIP_TESTS     set to 1 to skip the local test run
#
# Only committed files are deployed (git archive), so uncommitted edits never reach the VM.
set -euo pipefail

DEPLOY_HOST="${DEPLOY_HOST:?Set DEPLOY_HOST, e.g. DEPLOY_HOST=ubuntu@<vm-ip>}"
DEPLOY_KEY="${DEPLOY_KEY:-$HOME/.ssh/id_ed25519}"
APP_DIR="${APP_DIR:-/opt/healthbot}"
SERVICE="${SERVICE:-healthbot}"
BACKUP_DIR="${BACKUP_DIR:-/opt/healthbot-backups}"
HEALTH_TIMEOUT="${HEALTH_TIMEOUT:-240}"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

PATHS=(app data/kb data/training web requirements.txt)
SSH=(ssh -o BatchMode=yes -o ConnectTimeout=20 -i "$DEPLOY_KEY" "$DEPLOY_HOST")

cd "$(git rev-parse --show-toplevel)"
SHA="$(git rev-parse --short HEAD)"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="$BACKUP_DIR/pre-$SHA-$STAMP.tgz"

if ! git diff --quiet HEAD -- "${PATHS[@]}"; then
  echo "Refusing to deploy: uncommitted changes in ${PATHS[*]}. Commit them first." >&2
  exit 1
fi

if [ "$DRY_RUN" = 1 ]; then
  echo "[dry run] would deploy commit $SHA to $DEPLOY_HOST:$APP_DIR"
  echo "[dry run] files that would be uploaded (first 8):"
  git archive --format=tar HEAD -- "${PATHS[@]}" | tar -t | head -8 || true  # head closes the pipe early
  exit 0
fi

if [ "${SKIP_TESTS:-0}" != 1 ]; then
  echo "0/4 Running tests locally"
  PYTHONPATH="$PWD" python -m pytest tests -q
fi

rollback() {
  echo "Deploy failed. Rolling back to the backup taken before this deploy." >&2
  "${SSH[@]}" "sudo tar -xzf '$BACKUP' -C '$APP_DIR' && sudo systemctl restart '$SERVICE'" || true
  echo "Rolled back from $BACKUP. Check the service with: journalctl -u $SERVICE -n 50" >&2
  exit 1
}

wait_healthy() {
  "${SSH[@]}" "for i in \$(seq 1 $((HEALTH_TIMEOUT / 5))); do
    curl -fsS -m 5 http://127.0.0.1:8000/api/health >/dev/null && exit 0; sleep 5; done; exit 1"
}

smoke_test() {
  # An emergency message must produce the emergency template (it contains the 108 ambulance number).
  "${SSH[@]}" "curl -fsS -m 90 -X POST http://127.0.0.1:8000/api/chat \
    -H 'Content-Type: application/json' \
    -d '{\"message\":\"my father has chest pain\",\"session_id\":\"deploy-smoke\"}'" | grep -q '108'
}

echo "Deploying commit $SHA to $DEPLOY_HOST:$APP_DIR"

echo "1/4 Backup -> $BACKUP"
"${SSH[@]}" "sudo mkdir -p '$BACKUP_DIR' && cd '$APP_DIR' && sudo tar -czf '$BACKUP' --ignore-failed-read ${PATHS[*]}"

echo "2/4 Upload"
git archive --format=tar HEAD -- "${PATHS[@]}" | "${SSH[@]}" "sudo tar -x -C '$APP_DIR'"

LOCAL_REQ="$(git show HEAD:requirements.txt | sha256sum | cut -d' ' -f1)"
REMOTE_REQ="$("${SSH[@]}" "sha256sum '$APP_DIR/requirements.txt' | cut -d' ' -f1" 2>/dev/null || true)"
if [ "$LOCAL_REQ" != "$REMOTE_REQ" ]; then
  echo "Note: requirements.txt differs from the VM copy. If dependencies changed, install them on the VM:" >&2
  echo "  $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt" >&2
fi

echo "3/4 Restart $SERVICE"
"${SSH[@]}" "sudo systemctl restart '$SERVICE'" || rollback

echo "4/4 Health check (waiting up to ${HEALTH_TIMEOUT}s for the model to load)"
wait_healthy || rollback
smoke_test || rollback

echo "Deploy OK: commit $SHA is live. Backup kept at $BACKUP"
