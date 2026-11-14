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


def emergency_response(lang):
    helpline = HELPLINES.get(lang, HELPLINES["en"])
    template = kb.msg(lang, "emergency")
    return template.replace("%HELPLINES%", helpline)


def self_harm_response(lang):
    return SELF_HARM_RESPONSES.get(lang, SELF_HARM_RESPONSES["en"])


def fact_check_note(lang):
    return FACT_CHECK_NOTES.get(lang, FACT_CHECK_NOTES["en"])


def disclaimer(lang):
    return kb.msg(lang, "disclaimer")
