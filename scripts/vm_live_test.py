import requests, json

BASE = "http://localhost:8000"

def test(label, msg, sid):
    r = requests.post(f"{BASE}/api/chat", json={"message": msg, "session_id": sid})
    d = r.json()
    print(f"\n=== {label} ===")
    print(f"  intent: {d.get('intent')} | lang: {d.get('language')} | flow: {d.get('flow')} | backend: {d.get('llm_backend')}")
    print(f"  reply: {d.get('reply','')[:200]}")
    if d.get('factcheck'):
        fc = d['factcheck']
        print(f"  verdict: {fc.get('verdict')} | confidence: {fc.get('confidence')}")

test("SYMPTOM (English)", "I have fever and bad headache for 2 days", "s1")
test("HINDI", "मुझे बुखार और सिरदर्द है", "s2")
test("FACT CHECK (Myth)", "fact check: drinking cow urine cures cancer", "s3")
test("FACT CHECK (Vaccine myth)", "fact check: vaccines cause autism", "s4")
test("EMERGENCY", "chest pain cant breathe help", "s5")
test("VACCINATION", "when should a baby get polio vaccine", "s6")
test("OUTBREAK", "any disease outbreak in pincode 110001", "s7")
test("DISEASE INFO", "what are symptoms of dengue fever", "s8")
test("HINGLISH", "mujhe thoda fever hai aur body mein dard hai", "s9")
test("GREETING", "hello", "s10")
