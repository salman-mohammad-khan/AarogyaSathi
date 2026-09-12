import subprocess
import time

def ollama_rss_mb():
    out = subprocess.run(["ps", "-eo", "rss,args"], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if "ollama serve" in line or ("ollama" in line and "runner" in line):
            parts = line.split()
            try:
                return int(parts[0]) // 1024, parts[1]
            except Exception:
                pass
    return None

import httpx

before = ollama_rss_mb()
print("ollama RSS before (MB):", before)

r = httpx.post(
    "http://127.0.0.1:11434/api/generate",
    json={"model": "qwen3:1.7b", "prompt": "hi", "stream": False,
          "options": {"num_predict": 3, "num_ctx": 4096}},
    timeout=60,
)
print("load with 4096:", r.status_code)
time.sleep(3)
after = ollama_rss_mb()
print("ollama RSS after 4096 ctx (MB):", after)

out = subprocess.run(["free", "-m"], capture_output=True, text=True).stdout
print(out.splitlines()[1])