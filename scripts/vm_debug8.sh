#!/bin/bash
cd /opt/healthbot
echo "=== deployed generator.py check ==="
grep -n "LLM_CLOUD_TIMEOUT_S\|def _post\|def _cloud_generate" app/core/generator.py
echo "=== call app's generator directly ==="
PYTHONPATH=/opt/healthbot ./venv/bin/python - <<'PYEOF'
import time
from app.core import generator
generator.reset_availability()
print("backend():", generator.backend())
print("is_available():", generator.is_available())

ctx = "Disease: malaria. Malaria is spread by Anopheles mosquitoes. Prevention: use nets, remove stagnant water."
q = "மலேரியா எப்படி பரவுகிறது?"

t = time.time()
r = generator.grounded_answer(ctx, q, "ta")
print(f"grounded_answer: {time.time()-t:.1f}s, backend={generator.last_backend()}, reply={r!r}")

t = time.time()
r2 = generator.generate(generator.SYSTEM_PROMPT, f"CONTEXT:\n{ctx}\n\nQUESTION: {q}\n\nAnswer in Tamil.", prefer_cloud=True)
print(f"generate(prefer_cloud=True): {time.time()-t:.1f}s, backend={generator.last_backend()}, reply={r2!r}")
PYEOF
