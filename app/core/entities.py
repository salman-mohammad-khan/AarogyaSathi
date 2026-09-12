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
    "suicide": ["suicide", "khudkushi", "आत्महत्या", "self harm", "kill myself", "jeena nahi"],
    "pregnancy_bleed": ["pregnancy bleeding", "garbhavati ko khoon", "गर्भावस्था में खून"],
    "severe_burn": ["severe burn", "burned badly", "jala hua", "जल गया", "burnt"],
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


def _is_negated(text_lower, pos):
    prefix = text_lower[max(0, pos - 30) : pos]
    words = prefix.replace(",", " ").replace(".", " ").split()
    return any(w in NEGATION_WORDS for w in words[-4:])


def find_symptoms(text):
    text_lower = text.lower()
    found = []
    for symptom, aliases in SYMPTOM_LEXICON.items():
        for alias in aliases:
            if alias in text_lower:
                pos = text_lower.find(alias)
                if not _is_negated(text_lower, pos):
                    found.append(symptom)
                    break
    return found


def find_red_flags(text):
    text_lower = text.lower()
    flags = []
    for flag, aliases in RED_FLAG_LEXICON.items():
        for alias in aliases:
            if alias in text_lower:
                flags.append(flag)
                break
    return flags


def find_disease(text):
    text_lower = text.lower()
    for disease, aliases in DISEASE_ALIASES.items():
        for alias in aliases:
            if alias in text_lower:
                return disease
    return None


def find_vaccine(text):
    text_lower = text.lower()
    for vaccine, aliases in VACCINE_ALIASES.items():
        for alias in aliases:
            if alias in text_lower:
                return vaccine
    return None
