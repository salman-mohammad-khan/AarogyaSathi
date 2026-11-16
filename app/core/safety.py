import re

from app.core import entities
from app.core import kb
from app.config import HELPLINES

# Tele-MANAS: the Government of India's free, 24x7 tele mental health helpline (Ministry of Health and Family Welfare).
SELF_HARM_RESPONSES = {
    "en": (
        "I'm really sorry you are feeling this way, and I'm glad you reached out. You do not have to face this alone.\n"
        "Please talk to someone right now: Tele-MANAS, India's free 24x7 mental health helpline, at 14416 "
        "(or 1800-891-4416). If you are in immediate danger, call 112 or go to the nearest hospital. "
        "If someone is with you, please stay with them."
    ),
    "hi": (
        "मुझे बहुत दुख है कि आप ऐसा महसूस कर रहे हैं, और अच्छा है कि आपने बात की। आप अकेले नहीं हैं।\n"
        "कृपया अभी किसी से बात करें: Tele-MANAS, भारत की मुफ़्त 24x7 मानसिक स्वास्थ्य हेल्पलाइन, 14416 "
        "(या 1800-891-4416)। अगर आप तुरंत खतरे में हैं तो 112 पर कॉल करें या नज़दीकी अस्पताल जाएँ। "
        "अगर कोई आपके साथ है, तो कृपया उनके साथ रहें।"
    ),
}

FACT_CHECK_NOTES = {
    "en": "If you wanted a forwarded message fact-checked, please send that claim again on its own and I will check it.",
    "hi": "अगर आप किसी फ़ॉरवर्ड संदेश की जाँच कराना चाहते थे, तो कृपया वह दावा अलग से भेजें, उसकी जाँच कर दी जाएगी।",
}


def check_red_flags(text):
    flags = entities.find_red_flags(text)
    return flags if flags else []


def is_self_harm(flags):
    return "suicide" in (flags or [])


# Words that show a Latin-script message is romanised Hindi. fastText often labels short romanised Hindi as another
# Indian language (one such message was labelled Kannada), so emergency replies check this list as well.
_HINGLISH_MARKERS = frozenset((
    "hai", "hain", "ho", "raha", "rahi", "rahe", "mein", "ko", "ne", "ka", "ki", "ke", "se", "par", "mere", "meri",
    "mera", "mujhe", "hum", "humare", "bhai", "behen", "bahan", "papa", "mummy", "maa", "beta", "beti", "dard",
    "seene", "sine", "chhati", "saap", "saanp", "kaat", "kaata", "liya", "gaya", "gayi", "nahi", "bahut", "bohot",
    "turant", "jaldi", "madad", "bachao", "behosh", "saans", "khoon", "zahar", "jahar", "bukhar",
    "hoon", "chahta", "chahti", "marna", "jeene", "jeena", "zindagi", "khatam", "mann", "khudkushi",
))
_WORD_RE = re.compile(r"[a-z]+")


def emergency_language(text, detected):
    """Pick the reply language for an emergency message.

    A message in a non-Latin script keeps the detected language, because the script itself decides it. A message in
    plain Latin letters can only be English or romanised Hindi for the rule-based emergency path, so a label for any
    other language is replaced: Hindi if the text has Hindi marker words, English if not. A detected "hi" or "en"
    is also corrected to Hindi when two or more marker words are present.
    """
    if any(ord(ch) > 0x24F and ch.isalpha() for ch in text):
        return detected
    hits = sum(1 for word in set(_WORD_RE.findall(text.lower())) if word in _HINGLISH_MARKERS)
    romanised_hindi = hits >= 2
    if detected == "hi" or romanised_hindi:
        return "hi"
    return "en"


# One condition-specific tip per red flag, shown only when that flag fired and the language has its own text.
FIRST_AID_KEYS = {"snake_bite": "emergency_snake_bite"}


def first_aid_tips(flags, lang):
    table = kb.messages().get(lang, {})
    tips = []
    for flag in flags or []:
        key = FIRST_AID_KEYS.get(flag)
        if key and table.get(key):
            tips.append(table[key])
    return tips


def emergency_response(lang, flags=None):
    helpline = HELPLINES.get(lang, HELPLINES["en"])
    lines = [*first_aid_tips(flags, lang), helpline]
    return kb.msg(lang, "emergency").replace("%HELPLINES%", "\n".join(lines))


def self_harm_response(lang):
    return SELF_HARM_RESPONSES.get(lang, SELF_HARM_RESPONSES["en"])


def fact_check_note(lang):
    return FACT_CHECK_NOTES.get(lang, FACT_CHECK_NOTES["en"])


def disclaimer(lang):
    return kb.msg(lang, "disclaimer")
