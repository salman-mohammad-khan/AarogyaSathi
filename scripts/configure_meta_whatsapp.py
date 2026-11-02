"""Apply staged WhatsApp files on the Oracle VM, preserving an exact backup.

Run with /opt/healthbot/venv/bin/python; never prints credential values.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import os
import shutil
import subprocess


def main():
    root = Path('/opt/healthbot')
    stage = root / '.whatsapp-setup'
    expected = {
        'app/config.py': 'e1b21db7ffdca1151f48c26f40a184b36e465a5dd6b79256c89573cf72b93cf5',
        'app/channels/whatsapp.py': '923c155acdad1bb39f55d63a4938865d977a20d23be83b6bb568714bb9a84a6a',
    }
    for name, digest in expected.items():
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != digest:
            raise SystemExit('Deployment stopped: remote source changed since inspection: ' + name)
    values = {}
    for line in (stage / '.env.whatsapp.local').read_text().splitlines():
        key, sep, value = line.partition('=')
        if sep and key.startswith('WHATSAPP_'):
            values[key] = value
    required = {'WHATSAPP_TOKEN', 'WHATSAPP_PHONE_ID', 'WHATSAPP_VERIFY_TOKEN',
                'WHATSAPP_APP_SECRET', 'WHATSAPP_API_VERSION'}
    if not required.issubset(values) or not all(values[k] for k in required):
        raise SystemExit('Deployment stopped: required channel settings are missing')
    backup = root / '.whatsapp-backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup.mkdir(parents=True, mode=0o700)
    os.chmod(backup.parent, 0o700)
    targets = {root / 'app/config.py': stage / 'config.py',
               root / 'app/channels/whatsapp.py': stage / 'whatsapp.py',
               root / 'tests/test_meta_webhook_security.py': stage / 'test_meta_webhook_security.py'}
    original_env = (root / '.env').read_text()
    for target in [*targets, root / '.env']:
        if target.exists():
            saved = backup / target.relative_to(root)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
    os.chmod(backup / '.env', 0o600)
    try:
        for target, source in targets.items():
            shutil.copy2(source, target)
        remaining = [line for line in original_env.splitlines()
                     if line.partition('=')[0].strip() not in values]
        env_temp = root / '.env.whatsapp-next'
        env_temp.write_text('\n'.join(remaining) + '\n' +
                            '\n'.join(k + '=' + v for k, v in values.items()) + '\n')
        os.chmod(env_temp, 0o600)
        env_temp.replace(root / '.env')
        subprocess.run([str(root / 'venv/bin/python'), '-m', 'pytest',
                        'tests/test_meta_webhook_security.py', '-q'], cwd=root, check=True)
    except Exception:
        for target in [*targets, root / '.env']:
            saved = backup / target.relative_to(root)
            if saved.exists():
                shutil.copy2(saved, target)
        raise
    print('WhatsApp configuration and channel checks passed. Backup:', backup)


if __name__ == '__main__':
    main()
