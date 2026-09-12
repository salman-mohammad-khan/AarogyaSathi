import re

try:
    import fasttext
    _FASTTEXT_AVAILABLE = True
except Exception:
    _FASTTEXT_AVAILABLE = False

from app.config import MODEL_DIR, LANG_DETECT_MODEL, SUPPORTED_LANGUAGES

_SCRIPT_RANGES = {
    "hi": (0x0900, 0x097F),
    "bn": (0x0980, 0x09FF),
    "pa": (0x0A00, 0x0A7F),
    "gu": (0x0A80, 0x0AFF),
    "or": (0x0B00, 0x0B7F),
    "ta": (0x0B80, 0x0BFF),
    "te": (0x0C00, 0x0C7F),
    "kn": (0x0C80, 0x0CFF),
    "ml": (0x0D00, 0x0D7F),
    "mr": (0x0900, 0x097F),
    "ur": (0x0600, 0x06FF),
}

_model = None
_loaded = False


def _load():
    global _model, _loaded
    if _loaded:
        return
    _loaded = True
    if _FASTTEXT_AVAILABLE:
        path = MODEL_DIR / LANG_DETECT_MODEL
        if path.exists():
            try:
                _model = fasttext.load_model(str(path))
            except Exception:
                _model = None
        else:
            _model = fasttext.load_model(LANG_DETECT_MODEL)


def _script_hint(text):
    counts = {}
    for ch in text:
        code = ord(ch)
        for lang, (lo, hi) in _SCRIPT_RANGES.items():
            if lo <= code <= hi:
                counts[lang] = counts.get(lang, 0) + 1
    if not counts:
        return None
    return max(counts, key=counts.get)


def _fasttext_lang(text):
    if _model is None:
        return None
    label = _model.predict(text.replace("\n", " "), k=1)[0][0]
    return label.replace("__label__", "")[:2]


def detect_language(text):
    text = text.strip()
    if not text:
        return "en"
    script = _script_hint(text)
    if script:
        return script
    ft = _fasttext_lang(text) if _model is not None else None
    if ft in SUPPORTED_LANGUAGES:
        return ft
    if ft == "mr" and script is None:
        return "hi"
    return "en"


def transliterate_hint(text):
    hindi_word = r"\b(kya|hai|hain|kaise|kyu|mujhe|mere|mera|meri|tumhe|aapko|batao|bataye|karo|karna|kab|kaun|kitna|dava|bimari|bukhar|khansi|sardi|dast|ultie|sir|pet|dil|dawa|ilaaj|ilaj|laksahan|lakshan|bache|bacca|bacche|theek|thik|sahi|galat|sach|jhut|nahi|haan|acha|accha)\b"
    matches = re.findall(hindi_word, text.lower())
    return len(matches) >= 2
