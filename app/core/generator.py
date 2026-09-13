import os
import re
import time

import httpx

from app.config import (
    LLM_CLOUD_MAX_TOKENS,
    LLM_CLOUD_MODEL,
    LLM_CLOUD_TIMEOUT_S,
    LLM_MAX_TOKENS,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_TIMEOUT_S,
    OLLAMA_URL,
)

OLLAMA_CLOUD_URL = "https://ollama.com/api/chat"

_local_cooldown_until = 0.0
_last_backend = None

SYSTEM_PROMPT = (
    "You are AarogyaSathi, a public-health awareness assistant for rural India. "
    "STRICT RULES:\n"
    "1. Answer ONLY using the CONTEXT provided below the question.\n"
    "2. If the context does not contain the answer, say you do not have verified "
    "information and advise checking official sources (mohfw.gov.in, who.int).\n"
    "3. Keep the answer short: maximum 70 words.\n"
    "4. Answer in the language requested. If the question is in Hindi or Hinglish "
    "(Hindi written in English letters), reply in Hindi using Devanagari script.\n"
    "5. Never diagnose a disease for the user. Never prescribe medicines or dosages.\n"
    "6. If symptoms sound severe or urgent, tell the user to call 108/112 and see a doctor immediately.\n"
    "7. Use simple, respectful, village-friendly language.\n"
    "8. Never repeat the question back. Start directly with the answer.\n"
    "9. When the context lists possible conditions for symptoms, name the most "
    "relevant conditions from the context, then give the key advice from the context.\n"
    "10. Use short bullet lines for lists. Never merge unrelated facts into one sentence.\n"
    "11. For when-to-see-doctor advice, keep the context's wording: say 'if symptoms "
    "are severe, persistent or worsening'. Only say 'immediately' if the context says so.\n"
    "12. When replying in Hindi, use simple, common Hindi words (like कारण, लक्षण, बचाव, इलाज). "
    "Avoid rare or literary words.\n"
    "13. Frame possible conditions as 'could be related to ...'. Never write that the "
    "user 'has' a disease.\n"
    "14. Plain text only. Never use markdown (no **bold**, no ## headings, no bullet symbols). "
    "Separate points with new lines or commas."
)

PROBE_SYSTEM_PROMPT = (
    "You are AarogyaSathi, a public-health awareness assistant for rural India. "
    "You are collecting one small detail before sharing awareness information. "
    "Rules: 1) Ask exactly ONE short, empathetic question. "
    "2) Maximum 25 words. "
    "3) Use the requested language (Hindi in Devanagari script if the user writes Hinglish). "
    "4) Do not give any health advice yet. "
    "5) Do not repeat the user's words back."
)

GENERAL_SYSTEM_PROMPT = (
    "You are AarogyaSathi, a public-health assistant for rural India. The verified knowledge "
    "base does not cover this question. Answer briefly (maximum 60 words) from your general "
    "medical knowledge, in the requested language. Be safe: never diagnose a specific disease, "
    "never prescribe medicines or dosages. If you are not reasonably sure of the answer, reply "
    "with exactly the word UNSURE and nothing else."
)

SUMMARY_SYSTEM_PROMPT = (
    "You are a health assistant. Summarize the health conversation into 2-3 short lines that "
    "capture: symptoms mentioned, diseases or topics discussed, and what the user is asking "
    "about. Keep it factual and brief. No advice, no opinions."
)

UNDERSTAND_SYSTEM_PROMPT = (
    "You are the understanding module of a rural health chatbot. Analyze the user's message "
    "and reply with ONLY a valid JSON object, no other text. Fields:\n"
    '- "intent": one of "symptom", "disease_info", "prevention", "vaccination", "outbreak", '
    '"fact_check", "greeting", "help", "smalltalk", "thanks", "follow_up", "unclear", "other"\n'
    '- "symptoms": array of symptom names in lowercase English (e.g. ["fever","headache","neck pain"]). Empty if none.\n'
    '- "disease": disease name mentioned, or null\n'
    '- "duration": how long symptoms lasted if mentioned (e.g. "2 days"), or null\n'
    '- "clarification": true if the message is too unclear to act on\n'
    '- "follow_up": true if this is a short continuation of an earlier topic\n'
    "Rules: symptom = the user reports pain or illness (first person, e.g. \"I have fever\", \"my neck hurts\"). "
    "disease_info = asks about a disease. prevention = asks how to prevent something. "
    "fact_check = asks to verify a claim's truth. greeting = greeting only. "
    "follow_up = very short message continuing an earlier topic (e.g. \"2 days\", \"and fever?\", \"no\"). "
    "unclear = cannot tell what the user wants. "
    "EXCLUDE symptoms the user explicitly denies (e.g. \"no fever\" means fever is NOT a symptom). "
    "Keep symptom names in lowercase English."
)

SYMPTOM_ANALYSIS_SYSTEM_PROMPT = (
    "You are AarogyaSathi, a public-health awareness assistant for rural India. "
    "Analyze the user's reported symptoms and write a short, caring, plain-language analysis. Rules:\n"
    "1. Use ONLY the CONTEXT provided (symptoms, duration, possible conditions, doctor-seeking guidance).\n"
    "2. Frame conditions as 'could be related to ...'. Never say the user 'has' a disease.\n"
    "3. If the user said they do NOT have a symptom (e.g. no fever), acknowledge that and do not suggest it.\n"
    "4. Keep it calm and non-alarming. Do not prescribe medicines or dosages.\n"
    "5. End with the context's own advice on when to see a doctor.\n"
    "6. Answer in the requested language (Hindi in Devanagari). Maximum 90 words."
)


def understand_message(text, lang, extra_ctx=""):
    import json as _json

    reply = generate(
        UNDERSTAND_SYSTEM_PROMPT,
        f"{extra_ctx}USER MESSAGE: {text}\n\nReturn the JSON analysis.",
    )
    if not reply:
        return None
    try:
        m = re.search(r"\{.*\}", reply, re.DOTALL)
        if not m:
            return None
        data = _json.loads(m.group(0))
        if not isinstance(data, dict):
            return None
        return data
    except Exception:
        return None


def analyze_symptoms(context, lang, question):
    reply = generate(
        SYMPTOM_ANALYSIS_SYSTEM_PROMPT,
        f"CONTEXT:\n{context}\n\nUSER: {question}\n\nWrite the analysis in {_lang_name(lang)}.",
    )
    if not reply:
        return None
    cleaned = re.sub(r"\bUNSURE\b", "", reply, flags=re.IGNORECASE).strip()
    return cleaned or None


def summarize_conversation(history):
    conv = "\n".join(f"{h['role']}: {h['text']}" for h in history[-10:])
    reply = generate(
        SUMMARY_SYSTEM_PROMPT,
        f"Conversation:\n{conv}\n\nSummary (2-3 lines):",
    )
    if not reply:
        return None
    cleaned = re.sub(r"\bUNSURE\b", "", reply, flags=re.IGNORECASE).strip()
    return cleaned or None

UNSURE_MARKERS = [
    "does not provide", "does not contain", "no information", "no verified",
    "i don't have", "i do not have", "cannot answer", "can't answer", "not covered",
    "no context", "not mention", "no info", "does not mention",
    "not enough information", "no verified information", "context does not have",
    "not have verified", "unable to answer",
]


def looks_unsure(text):
    t = (text or "").lower().replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return any(m in t for m in UNSURE_MARKERS)


def general_answer(question, lang, extra_ctx=""):
    reply = generate(
        GENERAL_SYSTEM_PROMPT,
        f"{extra_ctx}QUESTION: {question}\n\nAnswer in {_lang_name(lang)}. If unsure, reply UNSURE.",
    )
    if not reply:
        return None
    cleaned = re.sub(r"\bUNSURE\b", "", reply, flags=re.IGNORECASE).strip()
    if not cleaned:
        return None
    return cleaned


def _lang_name(lang):
    return {
        "en": "English",
        "hi": "Hindi (Devanagari script)",
        "bn": "Bengali",
        "ta": "Tamil",
        "te": "Telugu",
        "mr": "Marathi",
        "gu": "Gujarati",
        "kn": "Kannada",
        "ml": "Malayalam",
        "pa": "Punjabi",
        "or": "Odia",
        "ur": "Urdu",
    }.get(lang, "the same language as the question")


def ask_followup(context, task, lang):
    return generate(
        PROBE_SYSTEM_PROMPT,
        f"CONTEXT:\n{context}\n\nTASK: {task}\n\nAnswer in {_lang_name(lang)}. Maximum 25 words.",
        prefer_cloud=lang not in ("en", "hi"),
    )

_availability = None


def is_available():
    global _availability
    if _availability is not None:
        return _availability
    _availability = _local_ok() or bool(os.environ.get("OLLAMA_API_KEY"))
    return _availability


def reset_availability():
    global _availability
    _availability = None


def _local_ok():
    if time.time() < _local_cooldown_until:
        return False
    try:
        resp = httpx.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def _local_failed():
    global _local_cooldown_until
    _local_cooldown_until = time.time() + 60


def last_backend():
    return _last_backend


def backend():
    if _local_ok():
        return "local"
    if os.environ.get("OLLAMA_API_KEY"):
        return "cloud"
    return None


def _post(url, payload, headers=None, timeout=LLM_TIMEOUT_S):
    try:
        resp = httpx.post(url, json=payload, headers=headers, timeout=timeout)
        if resp.status_code != 200:
            return None
        data = resp.json()
        content = (data.get("message") or {}).get("content", "").strip()
        return content or None
    except Exception:
        return None


def generate(system_prompt, user_prompt, prefer_cloud=False):
    global _last_backend
    if not is_available():
        _last_backend = None
        return None
    options = {
        "temperature": LLM_TEMPERATURE,
        "num_predict": LLM_MAX_TOKENS,
        "num_ctx": 4096,
    }
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    cloud_key = os.environ.get("OLLAMA_API_KEY")
    if cloud_key:
        result = _cloud_generate(messages, options)
        if result:
            _last_backend = "cloud"
            return result
    if _local_ok():
        payload = {
            "model": LLM_MODEL,
            "messages": messages,
            "stream": False,
            "think": False,
            "keep_alive": -1,
            "options": options,
        }
        result = _post(f"{OLLAMA_URL}/api/chat", payload)
        if result:
            _last_backend = "local"
            return result
        _local_failed()
    _last_backend = None
    return None


def _cloud_generate(messages, options):
    payload = {
        "model": LLM_CLOUD_MODEL,
        "messages": messages,
        "stream": False,
        "think": False,
        "options": {
            **options,
            "num_predict": LLM_CLOUD_MAX_TOKENS,
            "thinking": {"type": "disabled"},
        },
    }
    headers = {"Authorization": f"Bearer {os.environ['OLLAMA_API_KEY']}"}
    return _post(OLLAMA_CLOUD_URL, payload, headers, timeout=LLM_CLOUD_TIMEOUT_S)


def grounded_answer(context, question, lang="en"):
    user_prompt = (
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        f"Answer in {_lang_name(lang)}. Keep it under 70 words."
    )
    return generate(SYSTEM_PROMPT, user_prompt, prefer_cloud=lang not in ("en", "hi"))


FACTCHECK_EVAL_SYSTEM_PROMPT = (
    "You are an objective, evidence-based medical fact-checker for AarogyaSathi. "
    "You will receive a health CLAIM and LIVE WEB EVIDENCE from trusted fact-checkers and health authorities.\n"
    "Your job is to strictly compare the CLAIM against the EVIDENCE and reply with ONLY a valid JSON object, no other text.\n"
    "JSON Fields:\n"
    '- "verdict": exactly one of "MYTH" (if evidence refutes, disproves, or warns against the claim), '
    '"TRUE" (if evidence confirms the claim is scientifically accurate), '
    '"PARTLY_TRUE" (if evidence indicates mixed truth, supportive home remedy, or misleading context), '
    'or "UNVERIFIABLE" (if evidence does not address the claim).\n'
    '- "confidence": integer between 60 and 98 reflecting how clearly the evidence addresses the claim.\n'
    '- "explanation": concise 1-2 sentence factual explanation in the requested language. Be clear, calm, and objective. Never diagnose or prescribe.\n'
    '- "fear_mongering": boolean, true if the claim uses panic/alarmist language.\n'
    "STRICT RULES: Base your verdict ONLY on the provided evidence. If the evidence says 'false', 'hoax', 'myth', 'misleading', or 'no evidence', verdict MUST be MYTH or PARTLY_TRUE."
)


def evaluate_claim_evidence(claim, evidence_text, lang="en"):
    import json as _json

    user_prompt = (
        f"CLAIM: {claim}\n\n"
        f"VERIFIED WEB EVIDENCE:\n{evidence_text}\n\n"
        f"Evaluate the claim and return the JSON analysis in {_lang_name(lang)}."
    )
    reply = generate(FACTCHECK_EVAL_SYSTEM_PROMPT, user_prompt, prefer_cloud=True)
    if not reply:
        return None
    try:
        m = re.search(r"\{.*\}", reply, re.DOTALL)
        if not m:
            return None
        data = _json.loads(m.group(0))
        if not isinstance(data, dict):
            return None
        verdict = (data.get("verdict") or "").upper().strip()
        if verdict not in ("MYTH", "TRUE", "PARTLY_TRUE", "UNVERIFIABLE"):
            verdict = "UNVERIFIABLE"
        conf = float(data.get("confidence", 75.0))
        conf = max(40.0, min(99.0, conf))
        explanation = (data.get("explanation") or "").strip()
        if not explanation:
            return None
        return {
            "verdict": verdict,
            "confidence": conf,
            "explanation": explanation,
            "fear_mongering": bool(data.get("fear_mongering", False)),
        }
    except Exception:
        return None

