#!/bin/bash
# Append GOOGLE_FACTCHECK_API_KEY to VM .env if missing.
KEY="${1:-}"
if [ -z "$KEY" ]; then
  echo "Usage: sudo bash $0 <GOOGLE_FACTCHECK_API_KEY>"
  exit 1
fi
if grep -q '^GOOGLE_FACTCHECK_API_KEY=' /opt/healthbot/.env; then
  sed -i "s|^GOOGLE_FACTCHECK_API_KEY=.*|GOOGLE_FACTCHECK_API_KEY=$KEY|" /opt/healthbot/.env
else
  echo "GOOGLE_FACTCHECK_API_KEY=$KEY" >> /opt/healthbot/.env
fi
grep -c '^GOOGLE_FACTCHECK_API_KEY=' /opt/healthbot/.env
