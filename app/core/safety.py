from app.core import entities
from app.core import kb
from app.config import HELPLINES


def check_red_flags(text):
    flags = entities.find_red_flags(text)
    return flags if flags else []


def emergency_response(lang):
    helpline = HELPLINES.get(lang, HELPLINES["en"])
    template = kb.msg(lang, "emergency")
    return template.replace("%HELPLINES%", helpline)


def disclaimer(lang):
    return kb.msg(lang, "disclaimer")
