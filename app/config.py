import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env():
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if value and not os.environ.get(key):
            os.environ[key] = value


_load_env()
DATA_DIR = BASE_DIR / "data"
KB_DIR = DATA_DIR / "kb"
TRAINING_DIR = DATA_DIR / "training"
MODEL_DIR = DATA_DIR / "models"
EMBEDDING_CACHE_DIR = DATA_DIR / "embeddings"
WEB_DIR = BASE_DIR / "web"

EMBEDDING_MODEL = "sentence-transformers/LaBSE"
LANG_DETECT_MODEL = "lid.176.bin"
EMBEDDING_CACHE_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL = "http://127.0.0.1:11434"
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen3:1.7b")
LLM_CLOUD_MODEL = os.environ.get("LLM_CLOUD_MODEL", LLM_MODEL)
LLM_TIMEOUT_S = 30
LLM_CLOUD_TIMEOUT_S = int(os.environ.get("LLM_CLOUD_TIMEOUT_S", "120"))
LLM_TEMPERATURE = 0.1
LLM_MAX_TOKENS = 200
LLM_CLOUD_MAX_TOKENS = int(os.environ.get("LLM_CLOUD_MAX_TOKENS", "600"))

GOOGLE_FACTCHECK_API_KEY = os.environ.get("GOOGLE_FACTCHECK_API_KEY", "")
FACTCHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

SUPPORTED_LANGUAGES = ["en", "hi", "bn", "ta", "te", "mr", "gu", "kn", "ml", "pa", "or", "ur"]
LANG_NAMES = {
    "en": "English",
    "hi": "Hindi",
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
}

INTENT_CONFIDENCE_THRESHOLD = 0.55
RETRIEVAL_SIM_THRESHOLD = 0.52
FACTCHECK_SIM_THRESHOLD = 0.62
MAX_RETRIEVED = 5

HELPLINES = {
    "en": "National Health Helpline: 108 (Ambulance), 112 (Emergency), 104 (Health Advice).",
    "hi": "राष्ट्रीय स्वास्थ्य हेल्पलाइन: 108 (एम्बुलेंस), 112 (आपातकाल), 104 (स्वास्थ्य सलाह)।",
    "bn": "জাতীয় স্বাস্থ্য হেল্পলাইন: 108 (অ্যাম্বুলেন্স), 112 (জরুরি), 104 (স্বাস্থ্য পরামর্শ)।",
    "ta": "தேசிய சுகாதார உதவி எண்: 108 (ஆம்புலன்ஸ்), 112 (அவசரம்), 104 (சுகாதார ஆலோசனை).",
    "te": "జాతీయ ఆరోగ్య హెల్ప్‌లైన్: 108 (అంబులెన్స్), 112 (అత్యవసరం), 104 (ఆరోగ్య సలహా).",
    "mr": "राष्ट्रीय आरोग्य हेल्पलाइन: 108 (रुग्णवाहिका), 112 (आणीबाणी), 104 (आरोग्य सल्ला).",
    "gu": "રાષ્ટ્રીય આરોગ્ય હેલ્પલાઇન: 108 (એમ્બ્યુલન્સ), 112 (કટોકટી), 104 (આરોગ્ય સલાહ).",
    "kn": "ರಾಷ್ಟ್ರೀಯ ಆರೋಗ್ಯ ಸಹಾಯವಾಣಿ: 108 (ಆಂಬುಲೆನ್ಸ್), 112 (ತುರ್ತು), 104 (ಆರೋಗ್ಯ ಸಲಹೆ).",
    "ml": "ദേശീയ ആരോഗ്യ ഹെൽപ്പ്‌ലൈൻ: 108 (ആംബുലൻസ്), 112 (അടിയന്തരം), 104 (ആരോഗ്യ ഉപദേശം).",
    "pa": "ਰਾਸ਼ਟਰੀ ਸਿਹਤ ਹੈਲਪਲਾਈਨ: 108 (ਐਂਬੂਲੈਂਸ), 112 (ਐਮਰਜੈਂਸੀ), 104 (ਸਿਹਤ ਸਲਾਹ).",
    "or": "ଜାତୀୟ ସ୍ୱାସ୍ଥ୍ୟ ହେଲ୍ପଲାଇନ: 108 (ଆମ୍ବୁଲାନ୍ସ), 112 (ଜରୁରୀ), 104 (ସ୍ୱାସ୍ଥ୍ୟ ପରାମର୍ଶ).",
    "ur": "قومی صحت ہیلپ لائن: 108 (ایمبولینس)، 112 (ہنگامی)، 104 (صحت مشورہ).",
}
