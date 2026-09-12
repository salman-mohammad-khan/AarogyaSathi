import time

from app.core import kb, intent, retriever
from app.core.router import process_message
from app.factcheck import verifier

kb.load()
intent.load()
verifier._ensure_index()
t0 = time.time()
retriever._ensure_index()
print(f"index built in {time.time()-t0:.1f}s")

tests = [
    "hi",
    "tell me about dengue",
    "डेंगू से कैसे बचें?",
    "I have fever and headache",
    "mujhe bukhar aur sar dard hai",
    "vaccines for 6 week baby",
    "fact check: garlic cures dengue",
    "fact check: मोबाइल फोन से ब्रेन कैंसर होता है",
    "any dengue alert near me?",
    "my father is having chest pain",
    "how to make ORS at home",
]

for t in tests:
    start = time.time()
    r = process_message(t)
    ms = int((time.time() - start) * 1000)
    meta = r["meta"]
    line = r["text"].replace("\n", " | ")
    print(f"--- [{ms}ms] Q: {t}")
    print(f"    intent={meta.get('intent')} lang={meta.get('lang')} reply: {line[:250]}")
