import json
import time

from app.config import TRAINING_DIR
from app.core import intent, kb, retriever
from app.factcheck import verifier

kb.load()
intent.load()
verifier._ensure_index()
retriever._ensure_index()

with open(TRAINING_DIR / "eval.json", encoding="utf-8") as f:
    eval_data = json.load(f)

print("=" * 60)
print("EVALUATION REPORT - AarogyaSathi")
print("=" * 60)

intent_correct = 0
intent_total = 0
per_intent = {}
for item in eval_data["intent_eval"]:
    pred, conf = intent.predict_intent(item["text"], 0.45)
    intent_total += 1
    expected = item["intent"]
    per_intent.setdefault(expected, [0, 0])
    per_intent[expected][1] += 1
    if pred == expected:
        intent_correct += 1
        per_intent[expected][0] += 1
intent_acc = intent_correct / intent_total * 100
print(f"\n1. INTENT CLASSIFICATION (TF-IDF + Logistic Regression)")
print(f"   Accuracy: {intent_acc:.1f}% ({intent_correct}/{intent_total})")
for name, (ok, tot) in sorted(per_intent.items()):
    print(f"   - {name:16s} {ok}/{tot}")

ret_correct = 0
ret_total = 0
for item in eval_data["retrieval_eval"]:
    results = retriever.retrieve(item["text"], top_k=3, threshold=0.35)
    ret_total += 1
    if results and results[0]["type"] == item["expected_type"] and results[0]["id"] == item["expected_id"]:
        ret_correct += 1
    else:
        got = f"{results[0]['type']}:{results[0]['id']}" if results else "none"
        print(f"   MISS: {item['text']!r} -> {got} (expected {item['expected_type']}:{item['expected_id']})")
ret_acc = ret_correct / ret_total * 100
print(f"\n2. CROSS-LINGUAL RETRIEVAL (LaBSE embeddings)")
print(f"   Top-1 accuracy: {ret_acc:.1f}% ({ret_correct}/{ret_total})")

fc_correct = 0
fc_total = 0
start = time.time()
for item in eval_data["factcheck_eval"]:
    result = verifier.verify_claim(item["claim"])
    fc_total += 1
    if result["verdict"] == item["expected"]:
        fc_correct += 1
    else:
        print(f"   MISS: {item['claim']!r} -> {result['verdict']} (expected {item['expected']})")
fc_acc = fc_correct / fc_total * 100
fc_time = (time.time() - start) / fc_total
print(f"\n3. HEALTH-CLAIM FACT CHECK (myth corpus + LaBSE similarity)")
print(f"   Accuracy: {fc_acc:.1f}% ({fc_correct}/{fc_total}), avg {fc_time*1000:.0f} ms/claim")

print("\n" + "=" * 60)
print(f"TARGET (SIH25049): >=80% query-answer accuracy")
print(f"RESULT: intent {intent_acc:.1f}% | retrieval {ret_acc:.1f}% | fact-check {fc_acc:.1f}%")
print("=" * 60)
