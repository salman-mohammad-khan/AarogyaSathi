import re
import unicodedata

SYMPTOM_LEXICON = {
    "fever": ["fever", "bukhar", "बुखार", "ज्वर", "high temperature", "tapman"],
    "headache": ["headache", "sar dard", "sir dard", "सिरदर्द", "सिर में दर्द", "head pain", "headake", "hedache", "head ache", "sar dardh"],
    "cough": ["cough", "khansi", "खाँसी", "खांसी"],
    "cold": ["cold", "runny nose", "sardi", "zukam", "जुकाम", "ज़ुकाम", "सर्दी", "naak behna", "नाक बहना"],
    "sore_throat": ["sore throat", "gale me dard", "gale mein dard", "गले में दर्द", "गले में खराश"],
    "body_pain": ["body pain", "body ache", "badan dard", "मांसपेशियों में दर्द", "बदन दर्द", "शरीर में दर्द", "muscle pain"],
    "joint_pain": ["joint pain", "jodo me dard", "जोड़ों में दर्द", "जोड़ों का दर्द"],
    "nausea": ["nausea", "ji michlana", "मतली", "जी मिचलाना", "उबकाई", "feeling sick"],
    "vomiting": ["vomiting", "ulti", "उल्टी", "vomit", "उलटी"],
    "diarrhoea": ["diarrhoea", "diarrhea", "loose motions", "dast", "दस्त", "loose stool", "अतिसार"],
    "abdominal_pain": ["stomach pain", "pet dard", "pet me dard", "पेट दर्द", "पेट में दर्द", "abdominal pain", "stomach ache", "cramps", "marod", "मरोड़", "stoamch", "stomache", "stomuch", "stomch", "pet me dardh", "tummy", "tummy pain", "pet kharab", "पेट खराब", "pet kharaab", "stomach upset", "pet me jalan", "पेट में जलन"],
    "rash": ["rash", "rashes", "chakte", "चकत्ते", "त्वचा पर दाने", "dane", "दाने", "skin rash"],
    "fatigue": ["fatigue", "tired", "thakan", "थकान", "weakness", "kamzori", "कमज़ोरी", "कमजोरी", "sust", "सुस्त"],
    "dizziness": ["dizzy", "chakkar", "चक्कर", "dizziness", "vertigo", "ghoomna"],
    "breathlessness": ["breathless", "saans phoolna", "साँस फूलना", "सांस लेने में दिक्कत", "difficulty breathing", "saanas", "shortness of breath"],
    "chest_pain": ["chest pain", "chhati me dard", "सीने में दर्द", "छाती में दर्द"],
    "eye_pain": ["eye pain", "aankh dard", "आँखों में दर्द", "pain behind eyes", "आँखों के पीछे दर्द"],
    "jaundice_sign": ["yellow eyes", "yellow skin", "peeliya", "पीलिया", "peela", "पीला पेशाब", "dark urine", "गहरे रंग का पेशाब"],
    "weight_loss": ["weight loss", "wajan kam", "वज़न घटना", "वजन कम", "waight loss"],
    "night_sweats": ["night sweats", "raat me pasina", "रात में पसीना"],
    "blood_sputum": ["blood in sputum", "balgam me khoon", "बलगम में खून", "khoon ki khansi"],
    "bleeding": ["bleeding", "khoon behna", "खून बहना", "रक्तस्राव", "nose bleed", "nakseer", "नकसीर"],
    "loss_appetite": ["loss of appetite", "bhookh kam", "bhookh nahi", "भूख न लगना", "भूख कम"],
    "dehydration": ["dehydration", "pani ki kami", "पानी की कमी", "sunken eyes", "dhasi aankhein", "धँसी आँखें"],
    "unconscious": ["unconscious", "behosh", "बेहोश", "faint", "fainted", "collapse"],
    "seizure": ["seizure", "fits", "daure", "दौरे", "दौरा", "convulsion", "jhatke"],
    "swelling": ["swelling", "sujan", "सूजन", "सूजी"],
    "neck_pain": ["neck pain", "neck ache", "neck me dard", "gardan me dard", "गर्दन में दर्द", "neck stiffness", "गर्दन अकड़न"],
    "back_pain": ["back pain", "backache", "kamar dard", "कमर दर्द", "कमर में दर्द", "back me dard"],
    "shoulder_pain": ["shoulder pain", "kandhe me dard", "कंधे में दर्द", "kandha dard"],
    "leg_pain": ["leg pain", "leg me dard", "पैर में दर्द", "pair me dard", "foot pain"],
    "arm_pain": ["arm pain", "hand pain", "haath me dard", "बाँह में दर्द"],
    "knee_pain": ["knee pain", "ghutne me dard", "घुटने में दर्द"],
}

RED_FLAG_LEXICON = {
    "chest_pain": ["chest pain", "heart attack", "sine me dard", "सीने में दर्द", "chhati me dard", "dil ka daura", "दिल का दौरा"],
    "breathing": ["cannot breathe", "can't breathe", "difficulty breathing", "saans nahi aa rahi", "साँस नहीं आ रही", "सांस लेने में तकलीफ", "dum ghut raha hai", "दम घुट रहा है"],
    "unconscious": ["unconscious", "behosh", "बेहोश", "not responding", "unresponsive", "fainted", "collapse"],
    "seizure": ["seizure", "fits", "daure", "दौरे", "convulsions"],
    "bleeding": ["heavy bleeding", "khoon beh raha", "खून बह रहा", "severe bleeding", "profuse bleeding"],
    "snake_bite": ["snake bite", "snakebite", "saap ne kaat", "साँप ने काट", "saanp kaata", "सर्पदंश"],
    "rabid_animal": ["dog bite", "kutta kaat", "कुत्ते ने काट", "monkey bite", "bandar ne kaat", "बंदर ने काट"],
    "poison": ["poison", "zahar", "ज़हर", "जहर", "consumed poison", "jahar kha liya"],
    "stroke": ["stroke", "paralysis", "lakwa", "लकवा", "face drooping", "slurred speech"],
    "suicide": [
        "suicide", "khudkushi", "आत्महत्या", "self harm", "self-harm", "kill myself", "jeena nahi",
        "end my life", "ending my life", "end it all", "want to die", "wanna die", "take my own life",
        "don't want to live", "dont want to live", "no reason to live",
        "marna chahta", "marna chahti", "mar jana chahta", "mar jaana chahta", "mar jana chahti",
        "jeene ka mann nahi", "jine ka mann nahi", "zindagi khatam",
        "मरना चाहता", "मरना चाहती", "जीने का मन नहीं", "जिंदगी खत्म", "ज़िंदगी खत्म",
    ],
    "pregnancy_bleed": ["pregnancy bleeding", "garbhavati ko khoon", "गर्भावस्था में खून"],
    "severe_burn": ["severe burn", "burned badly", "jala hua", "जल गया"],
}

# Natural phrasings that a fixed phrase list cannot cover ("a snake just bit my brother", "seene mein dard ho raha
# hai"). Each pattern joins two cue words with at most three other words and no sentence punctuation between them, so
# "is that snake poisonous" and "snake sightings in my village" stay information questions. Plain regex, no model.
_GAP = r"(?:\s+[^\s.,;:!?]+){0,3}?"
_BITE = (
    r"(?:bit|bite|bites|biting|bitten|kaat|kaata|kaati|kaatna|kaatne|kata|dasa|daans|dans|"
    r"काट|काटा|काटी|डस|डसा|डसी)"
)
_SNAKE = r"(?:snakes?|cobra|viper|krait|saap|saanp|sanp|sap|साँप|सांप|सर्प)"
_ANIMAL = r"(?:dogs?|puppy|monkeys?|kutta|kutte|bandar|कुत्ता|कुत्ते|बंदर)"
_CHEST = r"(?:chest|seene|seena|sine|sina|chhati|chhaati|chati|chaati|सीने|सीना|छाती)"
_CHEST_SYMPTOM = (
    r"(?:pains?|hurt|hurts|hurting|ache|aching|tight|tightness|heavy|heaviness|pressure|crushing|burning|squeez\w*|"
    r"dard|dardh|dabav|bhaari|bhari|jalan|jakdan|दर्द|जलन|भारीपन|दबाव|जकड़न)"
)
_ASCII_WORD = r"(?<![a-z0-9])"  # left edge: do not start in the middle of an ASCII word
_ASCII_END = r"(?![a-z0-9])"

RED_FLAG_PATTERNS = {
    "snake_bite": [
        re.compile(rf"{_ASCII_WORD}{_SNAKE}{_GAP}\s+{_BITE}{_ASCII_END}"),
        re.compile(rf"{_ASCII_WORD}{_BITE}{_GAP}\s+{_SNAKE}{_ASCII_END}"),
    ],
    "rabid_animal": [
        re.compile(rf"{_ASCII_WORD}{_ANIMAL}{_GAP}\s+(?:bit|bites|bitten|kaat|kaata|kaati|काट|काटा|काटी){_ASCII_END}"),
        re.compile(rf"{_ASCII_WORD}(?:bit|bitten){_GAP}\s+(?:by\s+)?(?:an?\s+|the\s+)?{_ANIMAL}{_ASCII_END}"),
    ],
    "chest_pain": [
        re.compile(rf"{_ASCII_WORD}{_CHEST}{_GAP}\s+{_CHEST_SYMPTOM}{_ASCII_END}"),
        re.compile(rf"{_ASCII_WORD}{_CHEST_SYMPTOM}\s+(?:in|on|around)\s+(?:my\s+|his\s+|her\s+|the\s+)?chest{_ASCII_END}"),
    ],
}

DISEASE_ALIASES = {
    "dengue": ["dengue", "डेंगू", "dengu", "breakbone fever"],
    "malaria": ["malaria", "मलेरिया", "maleriya"],
    "typhoid": ["typhoid", "टाइफाइड", "enteric fever", "miyadi bukhar", "मियादी बुखार"],
    "cholera": ["cholera", "हैज़ा", "haiza", "हैजा"],
    "diarrhoea": ["diarrhoea", "diarrhea", "dast", "दस्त", "loose motion", "अतिसार"],
    "tuberculosis": ["tuberculosis", "tb", "टीबी", "क्षय रोग", "tapedik", "तपेदिक"],
    "hepatitis": ["hepatitis", "हेपेटाइटिस", "jaundice", "पीलिया", "peeliya"],
    "covid19": ["covid", "covid19", "covid-19", "कोविड", "corona", "कोरोना", "coronavirus"],
    "influenza": ["influenza", "flu", "फ्लू", "इन्फ्लूएंजा", "seasonal flu", "mausami bukhar"],
    "pneumonia": ["pneumonia", "निमोनिया", "nimonia"],
    "measles": ["measles", "खसरा", "khasra", "चेचक"],
    "rabies": ["rabies", "रेबीज़", "dog bite disease", "rabis"],
    "heatstroke": ["heatstroke", "heat stroke", "लू", "loo", "loot", "sun stroke", "हीट स्ट्रोक"],
    "anaemia": ["anaemia", "anemia", "एनीमिया", "khoon ki kami", "खून की कमी", "low hemoglobin", "low hb"],
}

VACCINE_ALIASES = {
    "bcg": ["bcg", "बीसीजी"],
    "hepb": ["hepatitis b", "hep b", "हेपेटाइटिस बी"],
    "opv": ["polio", "polio drops", "opv", "पोलियो", "पोलियो ड्रॉप"],
    "pentavalent": ["pentavalent", "5 in 1", "पेंटावेलेंट", "dpt", "डीपीटी"],
    "rotavirus": ["rotavirus", "रोटावायरस", "rotavac"],
    "pcv": ["pcv", "pneumococcal", "न्यूमोकोकल"],
    "ipv": ["ipv", "injectable polio", "आईपीवी"],
    "mr": ["mr vaccine", "measles vaccine", "खसरा टीका", "measles rubella", "एमआर टीका"],
    "je": ["je vaccine", "japanese encephalitis", "जापानी इंसेफेलाइटिस"],
    "dpt_booster": ["booster", "बूस्टर"],
    "td": ["td vaccine", "tetanus", "टिटनेस", "tt injection", "टीटी इंजेक्शन"],
    "covid_vaccine": ["covid vaccine", "corona vaccine", "कोविड टीका", "covidshield", "covaxin", "कोवैक्सिन"],
    "influenza_vaccine": ["flu vaccine", "influenza vaccine", "फ्लू टीका"],
}


NEGATION_WORDS = ["no", "not", "nahi", "nhi", "nahin", "कोई नहीं", "नहीं", "without", "koi nahi", "nahi hai"]


# Phrases that contain a red-flag word but are information topics, not emergencies.
RED_FLAG_CONTEXT_STRIPS = ("food poisoning",)

_SUFFIX_RE = re.compile(r"(?:s|es|ed|d|ing)(?![a-z0-9])")


def _ascii_alnum(ch):
    return ch.isascii() and ch.isalnum()


def _letter_like(ch):
    return unicodedata.category(ch)[0] in ("L", "M", "N")


def find_alias(text_lower, alias):
    """Return the index of `alias` in `text_lower` as a standalone term, or -1.

    English and Hinglish (ASCII) aliases must not touch an ASCII letter or digit, so "tb" does not match
    inside "outbreak", "fits" not inside "benefits" and "flu" not inside "influence". Aliases of five or more
    letters may take a plural or verb ending ("headaches", "coughing"). Very short non-ASCII aliases must not
    touch any letter or combining mark. Longer non-ASCII aliases keep plain substring matching, because
    Devanagari word forms are inflected and Python's word-boundary rules do not handle vowel marks.
    """
    ascii_alias = alias.isascii()
    if not ascii_alias and len(alias) > 3:
        return text_lower.find(alias)
    touches = _ascii_alnum if ascii_alias else _letter_like
    pos = text_lower.find(alias)
    while pos != -1:
        before = text_lower[pos - 1] if pos > 0 else ""
        rest = text_lower[pos + len(alias):]
        after = rest[:1]
        left_ok = not (before and touches(before))
        right_ok = not (after and touches(after))
        if not right_ok and ascii_alias and len(alias) >= 5 and _SUFFIX_RE.match(rest):
            right_ok = True
        if left_ok and right_ok:
            return pos
        pos = text_lower.find(alias, pos + 1)
    return -1


def contains_alias(text_lower, alias):
    return find_alias(text_lower, alias) != -1


def _is_negated(text_lower, pos):
    prefix = text_lower[max(0, pos - 30) : pos]
    words = prefix.replace(",", " ").replace(".", " ").split()
    return any(w in NEGATION_WORDS for w in words[-4:])


def find_symptoms(text):
    text_lower = text.lower()
    found = []
    for symptom, aliases in SYMPTOM_LEXICON.items():
        for alias in aliases:
            pos = find_alias(text_lower, alias)
            if pos != -1 and not _is_negated(text_lower, pos):
                found.append(symptom)
                break
    return found


def find_red_flags(text):
    text_lower = text.lower()
    for phrase in RED_FLAG_CONTEXT_STRIPS:
        text_lower = text_lower.replace(phrase, " ")
    flags = []
    for flag, aliases in RED_FLAG_LEXICON.items():
        if any(contains_alias(text_lower, alias) for alias in aliases) or any(
            pattern.search(text_lower) for pattern in RED_FLAG_PATTERNS.get(flag, ())
        ):
            flags.append(flag)
    return flags


def find_disease(text):
    text_lower = text.lower()
    for disease, aliases in DISEASE_ALIASES.items():
        for alias in aliases:
            if contains_alias(text_lower, alias):
                return disease
    return None


def find_vaccine(text):
    text_lower = text.lower()
    for vaccine, aliases in VACCINE_ALIASES.items():
        for alias in aliases:
            if contains_alias(text_lower, alias):
                return vaccine
    return None
