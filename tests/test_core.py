import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core import entities, intent, kb, language, safety

kb.load()
intent.load()


def test_intent_greeting():
    pred, conf = intent.predict_intent("namaste ji", 0.45)
    assert pred == "greeting"


def test_intent_disease_info_hindi():
    pred, conf = intent.predict_intent("डेंगू के बारे में बताओ", 0.45)
    assert pred == "disease_info"


def test_intent_symptom_check_hinglish():
    pred, conf = intent.predict_intent("mujhe bukhar aur sar dard hai", 0.45)
    assert pred == "symptom_check"


def test_intent_fact_check():
    pred, conf = intent.predict_intent("ye message sahi hai kya", 0.45)
    assert pred == "fact_check"


def test_intent_emergency():
    pred, conf = intent.predict_intent("saans lene me takleef hai", 0.45)
    assert pred == "emergency"


def test_red_flag_detection():
    flags = safety.check_red_flags("mere papa ko chest pain ho raha hai")
    assert flags
    assert "chest_pain" in flags


def test_red_flag_snake_bite():
    flags = safety.check_red_flags("saap ne kaat liya mujhe")
    assert "snake_bite" in flags


def test_symptom_extraction():
    syms = entities.find_symptoms("I have fever and headache")
    assert "fever" in syms
    assert "headache" in syms


def test_disease_entity():
    assert entities.find_disease("What are dengue symptoms?") == "dengue"
    assert entities.find_disease("टीबी क्या है") == "tuberculosis"


def test_language_detection():
    assert language.detect_language("What is malaria?") == "en"
    assert language.detect_language("नमस्ते आप कैसे हैं") == "hi"
    assert language.detect_language("மலேரியா எப்படி பரவுகிறது") == "ta"
    assert language.detect_language("మలేరియా ఎలా వ్యాపిస్తుంది") == "te"


def test_emergency_message_contains_helpline():
    msg = safety.emergency_response("en")
    assert "108" in msg


def test_disclaimer_present():
    assert "not a doctor" in safety.disclaimer("en")
