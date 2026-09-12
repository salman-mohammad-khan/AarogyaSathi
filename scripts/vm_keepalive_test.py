import httpx

payloads = [
    ("keep_alive string -1", {"model": "qwen3:1.7b", "messages": [{"role": "user", "content": "hi"}], "stream": False, "keep_alive": "-1"}),
    ("keep_alive int -1", {"model": "qwen3:1.7b", "messages": [{"role": "user", "content": "hi"}], "stream": False, "keep_alive": -1}),
    ("think false", {"model": "qwen3:1.7b", "messages": [{"role": "user", "content": "hi"}], "stream": False, "think": False}),
]

for name, p in payloads:
    try:
        r = httpx.post("http://127.0.0.1:11434/api/chat", json=p, timeout=30)
        body = r.text[:200]
        print(f"{name}: HTTP {r.status_code} | {body}")
    except Exception as e:
        print(f"{name}: EXC {e}")
