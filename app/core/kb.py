import json

from app.config import KB_DIR, LANG_NAMES

_DB = None


def load():
    global _DB
    if _DB is not None:
        return _DB
    _DB = {}
    for name in ["diseases", "vaccines", "faq", "myths", "alerts", "messages"]:
        with open(KB_DIR / f"{name}.json", encoding="utf-8") as f:
            _DB[name] = json.load(f)
    return _DB


def diseases():
    return load()["diseases"]["diseases"]


def vaccines():
    return load()["vaccines"]["vaccines"]


def faqs():
    return load()["faq"]["faqs"]


def myths():
    return load()["myths"]["myths"]


def alerts():
    return load()["alerts"]["alerts"]


def vaccine_summary():
    return load()["vaccines"]["schedule_summary"]


def messages():
    return load()["messages"]


def myth_meta():
    return load()["myths"]["meta"]


def msg(lang, key):
    table = messages()
    if lang in table and key in table[lang]:
        return table[lang][key]
    return table["en"].get(key, "")


def pick_lang(preferred, available):
    if preferred in available:
        return preferred
    if "hi" in available:
        return "hi"
    return "en"


def language_name(code):
    return LANG_NAMES.get(code, code)
