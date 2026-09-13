import sys
import time
import requests
import json

BASE = "http://localhost:8000"

TEST_CASES = [
    {
        "id": 1,
        "category": "Vaccine Myth",
        "query": "fact check: vaccines cause autism in children",
        "expected": "MYTH",
    },
    {
        "id": 2,
        "category": "Deadly First-Aid",
        "query": "fact check: put toothpaste or butter on burns to heal them",
        "expected": "MYTH",
    },
    {
        "id": 3,
        "category": "Viral WhatsApp Hoax",
        "query": "fact check: paracetamol contains deadly machupo virus",
        "expected": "MYTH",
    },
    {
        "id": 4,
        "category": "Indian Food / Pregnancy",
        "query": "fact check: eating ripe papaya causes miscarriage in pregnancy",
        "expected": ["MYTH", "PARTLY_TRUE"],
    },
    {
        "id": 5,
        "category": "Cancer Fake Cure",
        "query": "fact check: drinking cow urine cures cancer",
        "expected": ["MYTH", "PARTLY_TRUE"],
    },
    {
        "id": 6,
        "category": "Tech / Viral Conspiracy",
        "query": "fact check: 5G mobile towers spread coronavirus",
        "expected": "MYTH",
    },
    {
        "id": 7,
        "category": "Supportive Home Remedy",
        "query": "fact check: warm water with ginger and honey soothes mild cough",
        "expected": ["PARTLY_TRUE", "PARTLY TRUE"],
    },
    {
        "id": 8,
        "category": "True Medical Fact",
        "query": "fact check: female Aedes mosquitoes transmit dengue virus",
        "expected": ["TRUE", "VERIFIED"],
    },
    {
        "id": 9,
        "category": "True Immunization Fact",
        "query": "fact check: polio drops prevent infantile paralysis",
        "expected": ["TRUE", "VERIFIED"],
    },
    {
        "id": 10,
        "category": "Hindi Viral Claim",
        "query": "फैक्ट चेक: क्या गर्म पानी पीने से कोरोना खत्म हो जाता है",
        "expected": "MYTH",
    },
    {
        "id": 11,
        "category": "Hinglish Cancer Claim",
        "query": "ye sach hai kya: haldi doodh se cancer poori tarah theek ho jata hai",
        "expected": "MYTH",
    },
    {
        "id": 12,
        "category": "Snakebite Myth",
        "query": "fact check: suck venom out of snakebite with mouth",
        "expected": "MYTH",
    },
    {
        "id": 13,
        "category": "Animal Bite Myth",
        "query": "fact check: apply red chilli powder on dog bite to prevent rabies",
        "expected": "MYTH",
    },
    {
        "id": 14,
        "category": "Absurd / Unverifiable",
        "query": "fact check: eating 10 blue marbles every day cures diabetes",
        "expected": ["UNVERIFIABLE", "MYTH"],
    },
    {
        "id": 15,
        "category": "Dehydration Fact",
        "query": "fact check: ORS is the correct first treatment for diarrhoea",
        "expected": ["TRUE", "VERIFIED", "PARTLY_TRUE"],
    },
]

print("================================================================================")
print("     AAROGYASATHI AUTONOMOUS LIVE FACT-CHECKING ENGINE: 15-CLAIM TEST SUITE    ")
print("================================================================================")

results = []
passed = 0

for tc in TEST_CASES:
    cid = tc["id"]
    cat = tc["category"]
    query = tc["query"]
    exp = tc["expected"]
    exp_list = exp if isinstance(exp, list) else [exp]

    t0 = time.time()
    try:
        r = requests.post(
            f"{BASE}/api/chat",
            json={"message": query, "session_id": f"fc_test_{cid}"},
            timeout=35,
        )
        latency = round(time.time() - t0, 2)
        if r.status_code != 200:
            print(f"[{cid}/15] {cat}: HTTP {r.status_code} ({latency}s)")
            results.append({"id": cid, "cat": cat, "verdict": "ERROR", "ok": False, "latency": latency})
            continue

        data = r.json()
        fc = data.get("factcheck") or {}
        verdict = fc.get("verdict", "UNKNOWN")
        confidence = fc.get("confidence", 0.0)
        sources = fc.get("sources", [])
        is_live = fc.get("live", False)
        reply = data.get("reply", "")

        # Check match
        matched = (
            verdict in exp_list
            or (verdict == "TRUE" and "VERIFIED" in exp_list)
            or (verdict == "VERIFIED" and "TRUE" in exp_list)
        )
        if matched:
            passed += 1

        status_icon = "PASS" if matched else "FAIL"
        src_names = [s if isinstance(s, str) else s.get("name", "") for s in sources[:2]]
        src_str = ", ".join(src_names) if src_names else "Internal Corpus"

        print(f"\n[{cid:02d}/15] [{status_icon}] {cat} ({latency}s)")
        print(f"  Query:      {query}")
        print(f"  Verdict:    {verdict} (Confidence: {confidence}%) | Expected: {exp}")
        print(f"  Live Web:   {'YES (Real-time web search)' if is_live else 'NO (Curated KB / Safety Guard)'}")
        print(f"  Sources:    {src_str}")
        print(f"  Reply head: {reply[:160].replace(chr(10), ' ')}...")

        results.append({
            "id": cid,
            "cat": cat,
            "query": query,
            "verdict": verdict,
            "confidence": confidence,
            "expected": exp,
            "is_live": is_live,
            "sources": src_str,
            "ok": matched,
            "latency": latency,
        })
        time.sleep(2.5)

    except Exception as e:
        latency = round(time.time() - t0, 2)
        print(f"[{cid}/15] [FAIL] {cat}: Exception {e} ({latency}s)")
        results.append({"id": cid, "cat": cat, "verdict": "EXCEPTION", "ok": False, "latency": latency})

print("\n================================================================================")
print(f"                         SUMMARY: {passed}/15 TESTS PASSED                       ")
print("================================================================================")
for res in results:
    icon = "[OK]" if res["ok"] else "[X] "
    mode = "Live Web" if res.get("is_live") else "Curated/Guard"
    print(f"{icon} #{res['id']:02d} {res['cat'][:24]:24} -> Verdict: {res['verdict']:12} | Mode: {mode:14} ({res['latency']}s)")
print("================================================================================")
