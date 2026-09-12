import time

from app.core import kb, retriever

kb.load()
print("start", flush=True)
t0 = time.time()
retriever._ensure_index()
print(f"DONE kb {time.time() - t0:.1f}s", flush=True)
