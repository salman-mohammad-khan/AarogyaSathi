import time

from app.core import generator

generator.reset_availability()
print(f"LLM backend in use: {generator.backend()}")

start = time.time()
reply = generator.grounded_answer(
    "Dengue spreads via Aedes mosquitoes that bite during the day. Prevention: remove stagnant water, use nets.",
    "How can I prevent dengue?",
    "en",
)
if reply:
    print(f"Generation OK ({time.time() - start:.1f}s):")
    print(reply)
else:
    print("Generation FAILED (key invalid, quota exhausted, or network issue).")
    print("The bot will automatically fall back to template answers.")
