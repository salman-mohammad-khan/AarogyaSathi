import httpx
import time

# Direct local ollama test
t = time.time()
try:
    r = httpx.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": "qwen3:1.7b",
            "messages": [
                {"role": "system", "content": "You are a health assistant. Answer only from context."},
                {"role": "user", "content": "CONTEXT: Dengue is a mosquito-borne disease.\n\nQUESTION: what is dengue?\nAnswer in English."},
            ],
            "stream": False,
            "think": False,
            "keep_alive": "-1",
            "options": {"temperature": 0.1, "num_predict": 200, "num_ctx": 1024},
        },
        timeout=60,
    )
    print(f"local chat: HTTP {r.status_code} in {time.time()-t:.1f}s")
    print("content:", (r.json().get("message") or {}).get("content", "")[:120])
except Exception as e:
    print(f"local chat EXCEPTION: {type(e).__name__} {str(e)[:150]}")

# tags check
t = time.time()
try:
    r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=5)
    print(f"tags: HTTP {r.status_code} in {time.time()-t:.1f}s")
except Exception as e:
    print(f"tags EXCEPTION: {type(e).__name__} {str(e)[:100]}")
