import re
import urllib.parse

import httpx

WHITELIST_DOMAINS = [
    "wikipedia.org",
    "who.int",
    "cdc.gov",
    "nih.gov",
    "nlm.nih.gov",
    "medlineplus.gov",
    "mayoclinic.org",
    "clevelandclinic.org",
    "nhs.uk",
    "icmr.gov.in",
    "mohfw.gov.in",
    "nhm.gov.in",
    "hopkinsmedicine.org",
    "healthdirect.gov.au",
]

HEALTH_KEYWORDS = [
    "health", "medical", "doctor", "treatment", "medicine", "medic", "hospital", "clinic",
    "disease", "infection", "virus", "fever", "pain", "cough", "cold", "symptom", "headache",
    "stomach", "vomit", "diarrh", "pregnan", "vaccin", "diabetes", "blood", "pressure",
    "cholesterol", "heart", "lung", "skin", "rash", "allerg", "asthma", "immune", "immunity",
    "remedy", "herbal", "nutrition", "diet", "hygiene", "dengue", "malaria", "typhoid",
    "tuberculosis", "cancer", "jaundice", "hepatitis", "rabies", "measles", "cholera",
    "influenza", "flu", "pneumonia", "tb", "drug", "dose", "sugar", "weight", "anemia",
    "swelling", "numb", "dizzy", "breath", "bp", "surgery", "sick", "illness", "healthcare",
    "स्वास्थ्य", "बीमारी", "इलाज", "दवा", "बुखार", "दर्द", "खाँसी", "सर्दी", "लक्षण",
    "सिरदर्द", "पेट", "उल्टी", "दस्त", "गर्भ", "टीका", "मधुमेह", "रक्तचाप", "त्वचा",
    "एलर्जी", "अस्थमा", "रोग", "उपचार", "डॉक्टर", "चिकित्सक", "औषधि",
]


def is_health_query(text):
    t = (text or "").lower()
    return any(k in t for k in HEALTH_KEYWORDS)


def _domain(url):
    m = re.search(r"https?://([^/]+)", url or "")
    return m.group(1) if m else ""


def _wikipedia_summary(url):
    m = re.search(r"/wiki/([^#?]+)", url)
    if not m:
        return None
    title = urllib.parse.unquote(m.group(1).replace("_", " "))
    try:
        r = httpx.get(
            f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}",
            timeout=8,
        )
        if r.status_code != 200:
            return None
        extract = (r.json().get("extract") or "").strip()
        return extract[:600] if extract else None
    except Exception:
        return None


def search_health(query, max_results=8):
    if not is_health_query(query):
        return None
    try:
        from ddgs import DDGS

        results = list(DDGS().text(query, region="in-en", max_results=max_results))
    except Exception:
        return None
    trusted = [
        r for r in results if any(d in _domain(r.get("href", "")) for d in WHITELIST_DOMAINS)
    ]
    for top in trusted:
        url = top.get("href", "")
        domain = _domain(url)
        title = (top.get("title") or "").strip()
        snippet = (top.get("body") or "").strip()
        answer = snippet
        source = domain
        if "wikipedia.org" in domain:
            summary = _wikipedia_summary(url)
            if summary:
                answer = summary
        if not answer:
            answer = title
        if is_health_query(answer) or is_health_query(title):
            return {"answer": answer, "url": url, "source": source, "title": title}
    return None
