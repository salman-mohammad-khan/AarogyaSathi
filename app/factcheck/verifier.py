import re
import urllib.parse

import httpx
import numpy as np

from app.config import (
    FACTCHECK_SEARCH_MAX_RESULTS,
    FACTCHECK_SIM_THRESHOLD,
)
from app.core import embeddings, generator, kb, websearch

_CLAIM_PREFIX = re.compile(
    r"^(fact\s*check\s*:?\s*|verify\s*(this\s*)?(message\s*)?:?\s*|check\s*this\s*:?\s*|kya\s+ye\s+sach\s+hai\s*:?\s*|फैक्ट\s*चेक\s*:?\s*|क्या\s*यह\s*सच\s*है\s*:?\s*|फैक्ट चेक\s*:?\s*)",
    re.IGNORECASE,
)
_FORWARD_PREFIX = re.compile(r"^(forwarded|forwarded message|फॉरवर्डेड)\s*:?\s*", re.IGNORECASE)

_index = None

_VERDICT_LABELS = {
    "TRUE": "VERIFIED",
    "MYTH": "MYTH",
    "PARTLY_TRUE": "PARTLY TRUE",
    "UNVERIFIABLE": "UNVERIFIABLE",
}

TRUSTED_PUBLISHERS_TIER1 = {
    "pib fact check",
    "press information bureau",
    "who",
    "world health organization",
}

_RATING_MAP = [
    ("false", "MYTH"),
    ("fake", "MYTH"),
    ("hoax", "MYTH"),
    ("mostly false", "MYTH"),
    ("incorrect", "MYTH"),
    ("pants on fire", "MYTH"),
    ("no evidence", "MYTH"),
    ("unproven", "MYTH"),
    ("unsupported", "MYTH"),
    ("inaccurate", "MYTH"),
    ("fabricated", "MYTH"),
    ("false context", "PARTLY_TRUE"),
    ("misleading", "PARTLY_TRUE"),
    ("half true", "PARTLY_TRUE"),
    ("partly true", "PARTLY_TRUE"),
    ("mixed", "PARTLY_TRUE"),
    ("missing context", "PARTLY_TRUE"),
    ("mostly true", "TRUE"),
    ("true", "TRUE"),
    ("correct attribution", "TRUE"),
    ("correct", "TRUE"),
    ("verified", "TRUE"),
]

_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "can", "cure", "cures", "cure", "cured",
    "prevents", "prevent", "preventing", "of", "to", "and", "or", "for", "with", "by", "does",
    "do", "help", "good", "bad", "you", "i", "it", "in", "on", "that", "this", "your", "my",
    "what", "how", "why", "when", "where", "which", "who", "whom", "its", "treatment", "treat",
    "treats", "treated", "symptoms", "symptom", "cause", "causes", "caused", "prevention",
    "manage", "managing", "management", "tell", "about", "please", "know", "want", "need",
    "explain", "give", "some", "any", "me",
    "कर", "करता", "करती", "करते", "है", "हैं", "का", "के", "की", "को", "और", "यह", "वह",
    "में", "पर", "नहीं", "होता", "होती", "होते", "जाता", "जाती", "जाते", "देता", "देती",
    "से", "सब", "लिए", "क्या", "कि",
}

DISEASE_CANONICAL = {
    "covid": "covid",
    "corona": "covid",
    "coronavirus": "covid",
    "covid19": "covid",
    "covid-19": "covid",
    "कोविड": "covid",
    "कोरोना": "covid",
    "tb": "tb",
    "tuberculosis": "tb",
    "टीबी": "tb",
    "क्षय": "tb",
    "tapedik": "tb",
    "dengue": "dengue",
    "डेंगू": "dengue",
    "malaria": "malaria",
    "मलेरिया": "malaria",
    "typhoid": "typhoid",
    "टाइफाइड": "typhoid",
    "cholera": "cholera",
    "हैज़ा": "cholera",
    "हैजा": "cholera",
    "cancer": "cancer",
    "कैंसर": "cancer",
    "tumour": "cancer",
    "tumor": "cancer",
    "diabetes": "diabetes",
    "मधुमेह": "diabetes",
    "sugar": "diabetes",
    "rabies": "rabies",
    "रेबीज़": "rabies",
    "aids": "hiv",
    "hiv": "hiv",
    "एचआईवी": "hiv",
    "एड्स": "hiv",
    "hepatitis": "hepatitis",
    "jaundice": "hepatitis",
    "पीलिया": "hepatitis",
    "हेपेटाइटिस": "hepatitis",
    "polio": "polio",
    "पोलियो": "polio",
    "pneumonia": "pneumonia",
    "निमोनिया": "pneumonia",
    "measles": "measles",
    "खसरा": "measles",
    "heart attack": "cardiac",
    "stroke": "cardiac",
    "लकवा": "cardiac",
}

SEVERE_DISEASES = {"cancer", "tb", "rabies", "hiv", "cholera", "pneumonia", "polio", "cardiac"}

CURE_TERMS = [
    "cure", "cures", "curing", "cured", "treat", "treats", "treatment",
    "heal", "heals", "healing", "eradicate", "kill", "kills", "killing",
    "theek", "thik", "khatam", "khatm", "ilaj", "ilaaj", "jad se", "jar se", "dawa", "dawai",
    "इलाज", "ठीक", "जड़ से", "खत्म", "दवा"
]


def _disease_keys(s):
    s_lower = s.lower()
    keys = set()
    for alias, canonical in DISEASE_CANONICAL.items():
        if re.search(r"\b" + re.escape(alias) + r"\b", s_lower) or (len(alias) >= 4 and alias in s_lower):
            keys.add(canonical)
    return keys


def _stem_token(w):
    w = w.lower()
    for suffix in ("ing", "es", "ed", "s"):
        if len(w) > len(suffix) + 3 and w.endswith(suffix):
            return w[: -len(suffix)]
    return w


def _content_overlap(claim, ref):
    def tokens(s):
        raw = re.findall(r"[a-z0-9\u0900-\u097F]+", s.lower())
        return {_stem_token(w) for w in raw if w not in _STOPWORDS}
    a = tokens(claim)
    b = tokens(ref)
    if not a or not b:
        return 0.0
    common = len(a & b)
    dice = (2.0 * common) / (len(a) + len(b))
    query_cov = common / len(a)
    return min(dice, query_cov)


_REMEDY_KEYWORDS = [
    "kadha", "giloy", "tulsi", "haldi", "turmeric", "ginger", "adrak", "honey", "lemon",
    "garlic", "lahsun", "neem", "chyawanprash", "jeera", "ajwain", "saunf", "herbal",
    "natural remedy", "immunity", "immune", "boost", "remedy", "gharelu", "nuskha",
    "काढ़ा", "गिलोय", "तुलसी", "हल्दी", "अदरक", "लहसुन", "नीम", "च्यवनप्राश", "आयुर्वेदिक",
]


def _check_dangerous_first_aid(claim):
    c_lower = claim.lower()
    # Toothpaste / butter / ghee on burns
    if any(b in c_lower for b in ["burn", "burns", "जले", "जलना", "घाव"]) and any(
        t in c_lower for t in ["toothpaste", "butter", "oil", "ghee", "टूथपेस्ट", "मक्खन", "घी"]
    ):
        return {
            "verdict": "MYTH",
            "claim": claim,
            "confidence": 95.0,
            "explanation": {
                "en": "Toothpaste, butter, oil, or turmeric should NEVER be applied to burns. They trap heat inside the skin tissue, increase the risk of severe bacterial infection, and complicate clinical care. Correct immediate first aid: cool the burn under clean, running tap water for 15-20 minutes and seek medical care for deep or blistered burns.",
                "hi": "जले हुए हिस्से पर टूथपेस्ट, मक्खन, तेल या हल्दी कभी नहीं लगाना चाहिए। ये त्वचा में गर्मी को रोक लेते हैं, संक्रमण का गंभीर खतरा बढ़ाते हैं और घाव को बिगाड़ते हैं। सही प्राथमिक उपचार: जले हिस्से को 15-20 मिनट तक नल के साफ बहते पानी से ठंडा करें और गंभीर जलने पर तुरंत डॉक्टर को दिखाएं।",
            },
            "sources": [{"name": "WHO Burns Care", "tier": 1}, {"name": "MoHFW Burns Guidelines", "tier": 1}],
            "tags": ["first_aid", "dangerous"],
            "fear_mongering": False,
        }
    # Sucking / cutting snakebite
    if any(s in c_lower for s in ["snake", "snakebite", "साँप", "सर्प"]) and any(
        a in c_lower for a in ["suck", "mouth", "cut", "blade", "tourniquet", "चूस", "चीरा"]
    ):
        return {
            "verdict": "MYTH",
            "claim": claim,
            "confidence": 98.0,
            "explanation": {
                "en": "Never cut, suck venom with your mouth, or tie tight tourniquets on a snakebite. Sucking venom introduces mouth bacteria, cutting damages nerves/arteries, and tourniquets can cause tissue gangrene. Correct first aid: keep the victim calm and still, immobilize the limb with a loose splint, and rush to a hospital immediately for Anti-Snake Venom (ASV).",
                "hi": "सांप के काटे स्थान को कभी चीरा न लगाएं, मुंह से जहर न चूसें और न ही कसकर पट्टी बांधें। ऐसा करने से नसें कटने और गैंग्रीन का खतरा होता है। सही तरीका: मरीज को शांत रखें, काटे गए अंग को स्थिर रखें और तुरंत एंटी-स्नेक वेनम (ASV) के लिए नजदीकी सरकारी अस्पताल ले जाएं।",
            },
            "sources": [{"name": "WHO Snakebite Envenoming Guidelines", "tier": 1}, {"name": "National Health Portal", "tier": 1}],
            "tags": ["first_aid", "emergency", "dangerous"],
            "fear_mongering": False,
        }
    # Chilli / mud on dog bites
    if any(d in c_lower for d in ["dog", "kutta", "कुत्ता", "rabies", "रेबीज"]) and any(
        c in c_lower for c in ["chilli", "chili", "mirch", "mud", "cow dung", "मिर्च", "गोबर", "मिट्टी"]
    ):
        return {
            "verdict": "MYTH",
            "claim": claim,
            "confidence": 98.0,
            "explanation": {
                "en": "Applying red chilli powder, mud, or cow dung on animal bites is dangerous and does NOT prevent rabies. Rabies is 100% fatal once symptoms start. Immediate correct action: wash the bite thoroughly with soap and running water for at least 15 minutes, and visit a health center immediately for Anti-Rabies Vaccine (ARV) and rabies immunoglobulin if indicated.",
                "hi": "कुत्ते या जानवर के काटने पर लाल मिर्च, गोबर या मिट्टी लगाना बेहद खतरनाक है। लक्षण शुरू होने पर रेबीज 100% जानलेवा है। सही तरीका: घाव को तुरंत साबुन और बहते पानी से कम से कम 15 मिनट तक अच्छी तरह धोएं और तुरंत अस्पताल जाकर एंटी-रेबीज वैक्सीन (ARV) लगवाएं।",
            },
            "sources": [{"name": "National Rabies Control Programme (NRCP)", "tier": 1}, {"name": "WHO Rabies Guidelines", "tier": 1}],
            "tags": ["rabies", "first_aid", "dangerous"],
            "fear_mongering": False,
        }
    return None


def _remedy_fallback(claim):
    claim_lower = claim.lower()
    if not any(k in claim_lower for k in _REMEDY_KEYWORDS):
        return None

    # Medical Hazard Guard: Home remedy + severe disease + cure claim = MYTH!
    ck = _disease_keys(claim)
    has_cure_word = any(c in claim_lower for c in CURE_TERMS)
    if (ck & SEVERE_DISEASES) and has_cure_word:
        return {
            "verdict": "MYTH",
            "claim": claim,
            "confidence": 95.0,
            "explanation": {
                "en": "Dangerous Claim: Serious medical conditions like cancer, tuberculosis (TB), rabies, and HIV CANNOT be cured by home remedies, herbs, or kitchen ingredients. Relying on unproven home cures delays essential medical treatment and can be fatal. Always consult a qualified medical professional.",
                "hi": "खतरनाक दावा: कैंसर, टीबी (तपेदिक), रेबीज और एचआईवी जैसी गंभीर बीमारियों का इलाज घरेलू नुस्खों, जड़ी-बूटियों या रसोई की चीजों से नहीं हो सकता। अप्रमाणित घरेलू नुस्खों पर भरोसा करने से ज़रूरी डॉक्टरी इलाज में देरी होती है जो जानलेवा हो सकती है। हमेशा योग्य डॉक्टर से संपर्क करें।",
            },
            "sources": [{"name": "WHO Clinical Guidelines", "tier": 1}, {"name": "MoHFW / ICMR", "tier": 1}],
            "tags": ["dangerous_misinformation", "medical_safety"],
            "fear_mongering": False,
        }

    return {
        "verdict": "PARTLY_TRUE",
        "claim": claim,
        "confidence": 60.0,
        "explanation": {
            "en": "This is a traditional home remedy or supportive wellness practice. While traditional remedies like ginger, tulsi, and turmeric can offer comfort and soothe mild symptoms (like mild cough or sore throat), they do NOT cure major diseases or replace doctor-prescribed medicines. If symptoms are severe or persistent, consult a doctor.",
            "hi": "यह एक पारंपरिक घरेलू नुस्खा या सहायक स्वास्थ्य आदत है। हालांकि अदरक, तुलसी और हल्दी जैसे नुस्खे हल्के लक्षणों (जैसे हल्की खांसी या गले की खराश) में आराम दे सकते हैं, पर ये किसी बड़ी बीमारी को ठीक नहीं करते और न ही डॉक्टर की दवा का विकल्प हैं। यदि लक्षण गंभीर या लगातार बने रहें, तो डॉक्टर को दिखाएँ।",
        },
        "sources": [{"name": "WHO Traditional Medicine", "tier": 1}, {"name": "National Health Portal (India)", "tier": 1}],
        "tags": ["home_remedy", "supportive_wellness"],
        "fear_mongering": False,
    }


def _rating_to_verdict(rating):
    rating_lower = (rating or "").lower()
    for token, verdict in _RATING_MAP:
        if token in rating_lower:
            return verdict
    return "UNVERIFIABLE"


def _distill_query_keywords(claim):
    raw = re.findall(r"[a-z0-9\u0900-\u097F]+", claim.lower())
    words = [w for w in raw if w not in _STOPWORDS and len(w) > 2]
    return " ".join(words[:6]) if len(words) >= 2 else claim


TRUSTED_FACTCHECK_DOMAINS = [
    # Indian Fact-Checkers & Authorities
    "factcheck.pib.gov.in",
    "pib.gov.in",
    "thip.media",
    "boomlive.in",
    "vishwasnews.com",
    "altnews.in",
    "thequint.com",
    "thelogicalindian.com",
    "icmr.gov.in",
    "mohfw.gov.in",
    "nhm.gov.in",
    # Global Health Authorities
    "who.int",
    "cdc.gov",
    "nih.gov",
    "nlm.nih.gov",
    "medlineplus.gov",
    "mayoclinic.org",
    "clevelandclinic.org",
    "nhs.uk",
    "hopkinsmedicine.org",
    "healthdirect.gov.au",
    # Global Fact-Checkers
    "snopes.com",
    "afp.com",
    "factcheck.org",
    "reuters.com",
    "wikipedia.org",
]


def _extract_domain(url):
    m = re.search(r"https?://([^/]+)", url or "")
    return m.group(1).lower() if m else ""


def _search_wikipedia(query):
    headers = {"User-Agent": "AarogyaSathiHealthBot/1.0 (healthbot@aarogyasathi.org)"}
    q_clean = re.sub(r"^(fact\s*check|फैक्ट\s*चेक|ye\s*sach\s*hai\s*kya)[\s:]*", "", query, flags=re.I).strip()
    wiki_lang = "hi" if re.search(r"[\u0900-\u097F]", query) else "en"
    try:
        r = httpx.get(
            f"https://{wiki_lang}.wikipedia.org/w/api.php",
            params={"action": "query", "list": "search", "srsearch": q_clean, "format": "json", "srlimit": 3},
            headers=headers,
            timeout=FACTCHECK_SEARCH_TIMEOUT_S,
        )
        if r.status_code != 200:
            return []
        hits = r.json().get("query", {}).get("search", [])
        items = []
        for h in hits:
            title = h["title"]
            snippet = ""
            try:
                s_res = httpx.get(
                    f"https://{wiki_lang}.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}",
                    headers=headers,
                    timeout=FACTCHECK_SEARCH_TIMEOUT_S,
                )
                if s_res.status_code == 200:
                    snippet = s_res.json().get("extract", "")
            except Exception:
                pass
            if not snippet:
                snippet = re.sub(r"<[^>]+>", "", h.get("snippet", ""))
            if snippet:
                items.append({
                    "url": f"https://{wiki_lang}.wikipedia.org/wiki/{urllib.parse.quote(title)}",
                    "domain": "wikipedia.org",
                    "title": title,
                    "snippet": snippet[:600],
                    "tier": 1,
                })
        return items
    except Exception:
        return []


def _search_live_evidence(claim, max_results=FACTCHECK_SEARCH_MAX_RESULTS):
    if re.search(r"[\u0900-\u097F]", claim):
        queries = [f"{claim} फैक्ट चेक", f"fact check {claim}"]
    else:
        queries = [f"fact check {claim}"]

    collected = []
    seen_urls = set()

    try:
        from ddgs import DDGS
        ddgs = DDGS()
        for q in queries:
            try:
                results = list(ddgs.text(q, region="in-en", max_results=max_results))
                for r in results:
                    url = r.get("href", "")
                    if not url or url in seen_urls:
                        continue
                    seen_urls.add(url)
                    title = (r.get("title") or "").strip()
                    snippet = (r.get("body") or "").strip()
                    domain = _extract_domain(url)
                    is_trusted = any(td in domain for td in TRUSTED_FACTCHECK_DOMAINS)
                    has_fc_marker = any(
                        m in (title + " " + snippet).lower()
                        for m in ["fact check", "fact-check", "myth", "debunk", "hoax", "false", "misleading", "claim", "true", "evidence"]
                    )
                    if is_trusted or has_fc_marker:
                        collected.append({
                            "url": url,
                            "domain": domain,
                            "title": title,
                            "snippet": snippet,
                            "tier": 1 if is_trusted else 2,
                        })
            except Exception:
                pass

            if len(collected) < 2:
                try:
                    q_news = re.sub(r"^(fact\s*check|फैक्ट\s*चेक)[\s:]*", "", q, flags=re.I).strip()
                    news_results = list(ddgs.news(q_news, max_results=max_results))
                    for r in news_results:
                        url = r.get("url", "")
                        if not url or url in seen_urls:
                            continue
                        seen_urls.add(url)
                        title = (r.get("title") or "").strip()
                        snippet = (r.get("body") or "").strip()
                        domain = _extract_domain(url)
                        collected.append({
                            "url": url,
                            "domain": domain,
                            "title": title,
                            "snippet": snippet,
                            "tier": 2,
                        })
                except Exception:
                    pass

            if len(collected) >= 2:
                break
    except Exception:
        pass

    if not collected:
        try:
            wiki_items = _search_wikipedia(claim)
            for item in wiki_items:
                if item["url"] not in seen_urls:
                    seen_urls.add(item["url"])
                    collected.append(item)
        except Exception:
            pass

    if not collected:
        try:
            ws = websearch.search_health(f"fact check {claim}")
            if ws and ws.get("url") not in seen_urls:
                collected.append({
                    "url": ws.get("url", ""),
                    "domain": ws.get("source", ""),
                    "title": ws.get("title", ""),
                    "snippet": ws.get("answer", ""),
                    "tier": 1,
                })
        except Exception:
            pass

    return collected


def _live_lookup(claim, lang):
    evidence_items = _search_live_evidence(claim)
    if not evidence_items:
        return None

    evidence_parts = []
    sources = []
    for item in evidence_items[:3]:
        evidence_parts.append(
            f"Source: {item['domain']} | Headline: {item['title']}\nExcerpt: {item['snippet']}"
        )
        sources.append({
            "name": item["domain"],
            "title": item["title"],
            "url": item["url"],
            "tier": item["tier"],
        })
    evidence_text = "\n---\n".join(evidence_parts)

    evaluation = generator.evaluate_claim_evidence(claim, evidence_text, lang)
    if not evaluation:
        return None

    verdict = evaluation["verdict"]
    if verdict == "UNVERIFIABLE":
        return None

    explanation_text = evaluation["explanation"]
    explanation = {
        lang: explanation_text,
        "en": explanation_text,
    }

    return {
        "verdict": verdict,
        "claim": claim,
        "confidence": evaluation["confidence"],
        "explanation": explanation,
        "sources": sources,
        "tags": ["live_verification", "autonomous_factcheck"],
        "fear_mongering": evaluation.get("fear_mongering", False),
        "live": True,
    }


def clean_claim(text):
    text = _FORWARD_PREFIX.sub("", text.strip())
    text = _CLAIM_PREFIX.sub("", text.strip())
    return text.strip()


def _ensure_index():
    global _index
    if _index is not None:
        return _index
    claims = []
    entries = []
    for m in kb.myths():
        for lang in ["en", "hi"]:
            if lang in m.get("claim", {}):
                claims.append(m["claim"][lang])
                entries.append(m)
    matrix = embeddings.embed_with_cache("myth_claims", claims)
    _index = {"claims": claims, "entries": entries, "matrix": matrix}
    return _index


def _confidence_from(sim, tier):
    base = float(sim) * 100.0
    boost = 6.0 if tier == 1 else 2.0
    return round(min(99.0, base + boost), 1)


def verify_claim(text, lang="en"):
    index = _ensure_index()
    claim = clean_claim(text)
    if len(claim.split()) < 3:
        return {"verdict": "INVALID", "claim": text, "message_key": "factcheck_no_claim"}

    # 1. Fast safety check for critical harmful first-aid myths
    dangerous_fa = _check_dangerous_first_aid(claim)
    if dangerous_fa:
        return dangerous_fa

    qv = embeddings.embed_texts([claim])[0]
    sims = embeddings.cosine_similarity(qv, index["matrix"])

    # 2. Disease-aware re-ranking
    ck = _disease_keys(claim)
    scores = np.copy(sims)
    if ck:
        for i, entry in enumerate(index["entries"]):
            ek = _disease_keys(entry["claim"].get("en", "")) | _disease_keys(entry["claim"].get("hi", ""))
            if ek:
                if ck & ek:
                    scores[i] += 0.15  # same disease boost
                else:
                    scores[i] -= 0.30  # conflicting disease penalty

    # Re-rank top candidates by combining semantic similarity and lexical overlap
    top_candidates = np.argsort(scores)[::-1][:8]
    best_idx = int(top_candidates[0])
    best_combined = -1.0
    for idx in top_candidates:
        entry_cand = index["entries"][idx]
        ol = max(
            _content_overlap(claim, entry_cand["claim"].get("en", "")),
            _content_overlap(claim, entry_cand["claim"].get("hi", "")),
        )
        combined = float(scores[idx]) * (1.0 + 0.6 * ol)
        if combined > best_combined:
            best_combined = combined
            best_idx = int(idx)

    best_sim = float(sims[best_idx])
    entry = index["entries"][best_idx]

    overlap = max(
        _content_overlap(claim, entry["claim"].get("en", "")),
        _content_overlap(claim, entry["claim"].get("hi", "")),
    )
    ek = _disease_keys(entry["claim"].get("en", "")) | _disease_keys(entry["claim"].get("hi", ""))
    disease_conflict = bool(ck) and bool(ek) and not (ck & ek)

    use_curated = (
        (best_sim >= 0.70 and overlap >= 0.35 and not disease_conflict)
        or (best_sim >= FACTCHECK_SIM_THRESHOLD and overlap >= 0.40 and not disease_conflict)
    )

    if not use_curated:
        live = _live_lookup(claim, lang)
        if live:
            return live
        remedy = _remedy_fallback(claim)
        if remedy:
            return remedy
        return {
            "verdict": "UNVERIFIABLE",
            "claim": claim,
            "confidence": round(max(10.0, (1.0 - best_sim) * 100.0), 1),
            "explanation": {
                "en": "This claim is not in our verified corpus of common health myths, and no trusted fact-checker covered it, so I cannot give a confident verdict. Please check it on official sources: who.int, mohfw.gov.in, or PIB Fact Check (factcheck.pib.gov.in). Remember: health claims from unverified forwards should not be shared further without checking.",
                "hi": "यह दावा सामान्य स्वास्थ्य भ्रांतियों के हमारे सत्यापित संग्रह में नहीं है और किसी विश्वसनीय फैक्ट-चेकर ने इसे कवर नहीं किया, इसलिए मैं निश्चित फैसला नहीं दे सकता। कृपया आधिकारिक स्रोतों पर जाँचें: who.int, mohfw.gov.in या PIB फैक्ट चेक (factcheck.pib.gov.in)। याद रखें: बिना जाँचे अनजान फॉरवर्ड किए गए स्वास्थ्य दावे आगे साझा न करें।",
            },
            "sources": [{"name": "PIB Fact Check", "tier": 1}, {"name": "WHO", "tier": 1}],
            "fear_mongering": False,
        }

    tier = min(s["tier"] for s in entry.get("sources", [{"tier": 2}]))
    confidence = _confidence_from(best_sim, tier)
    return {
        "verdict": entry["verdict"],
        "claim": claim,
        "confidence": confidence,
        "similarity": best_sim,
        "explanation": entry["explanation"],
        "sources": entry["sources"],
        "tags": entry.get("tags", []),
        "fear_mongering": entry.get("fear_mongering", False),
        "matched_claim": entry["claim"],
    }


def format_verdict(result, lang):
    if result["verdict"] == "INVALID":
        return kb.msg(lang, "factcheck_no_claim")

    if lang not in ("en", "hi"):
        lang = "en"

    labels = {
        "TRUE": "VERIFIED",
        "VERIFIED": "VERIFIED",
        "MYTH": "MYTH",
        "PARTLY_TRUE": "PARTLY TRUE",
        "UNVERIFIABLE": "UNVERIFIABLE",
    }
    if lang == "hi":
        labels = {
            "TRUE": "सत्य",
            "VERIFIED": "सत्य",
            "MYTH": "भ्रांति",
            "PARTLY_TRUE": "आंशिक सत्य",
            "UNVERIFIABLE": "पुष्टि असंभव",
        }

    title = "[FACT CHECK]"
    if lang == "hi":
        title = "[फैक्ट चेक]"

    verdict_raw = result.get("verdict", "UNVERIFIABLE")
    verdict_label = labels.get(verdict_raw, verdict_raw)
    if result.get("fear_mongering"):
        suffix = " (with context - see explanation)" if lang == "en" else " (संदर्भ सहित - स्पष्टीकरण पढ़ें)"
        verdict_label += suffix

    lines = [
        f"{title} {verdict_label} | Confidence: {result['confidence']}%",
        f"Claim: {result['claim']}",
    ]
    if "matched_claim" in result and result["verdict"] != "UNVERIFIABLE":
        lines.append(f"Matched known claim: {result['matched_claim'].get(lang, result['matched_claim'].get('en', ''))}")
    explanation = result["explanation"].get(lang) or result["explanation"].get("en", "")
    lines.append(f"Explanation: {explanation}")
    src_list = []
    for s in result.get("sources", []):
        name = s.get("name", "")
        url = s.get("url")
        if url:
            src_list.append(f"{name} ({url})")
        else:
            tier_str = "Govt/WHO" if s.get("tier") == 1 else "Reputed institution"
            src_list.append(f"{name} ({tier_str})")
    lines.append(f"Sources: {', '.join(src_list)}")
    if result.get("tags"):
        lines.append(f"Category: {', '.join(result['tags'])}")
    lines.append(kb.msg(lang, "disclaimer"))
    return "\n".join(lines)
