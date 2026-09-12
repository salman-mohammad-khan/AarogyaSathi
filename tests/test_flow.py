import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core import generator, intent, kb
from app.core import session as session_store
from app.core.router import process_message

kb.load()
intent.load()
generator._availability = False


def test_smalltalk_intent():
    pred, _ = intent.predict_intent("who are you", 0.45)
    assert pred == "smalltalk"


def test_smalltalk_hindi_intent():
    pred, _ = intent.predict_intent("tum kaun ho", 0.45)
    assert pred == "smalltalk"


def test_symptom_probe_then_final():
    s = session_store.get_session("test1")
    s.clear()
    r1 = process_message("I have headache", session=s)
    assert r1["meta"]["flow"] == "symptom_probe"
    assert "days" in r1["text"].lower() or "दिनों" in r1["text"]
    r2 = process_message("since 2 days and I also have fever", session=s)
    assert r2["meta"]["flow"] == "symptom_final"
    assert "fever" in r2["meta"]["symptoms"]
    assert "typhoid" in r2["text"] or "malaria" in r2["text"] or "dengue" in r2["text"]


def test_flow_does_not_diagnose():
    s = session_store.get_session("test1b")
    s.clear()
    process_message("I have headache", session=s)
    r2 = process_message("2 days, no fever", session=s)
    assert "you have" not in r2["text"].lower()


def test_flow_interrupted_by_other_intent():
    s = session_store.get_session("test2")
    s.clear()
    process_message("pet me dard hai", session=s)
    r2 = process_message("tell me about dengue", session=s)
    assert r2["meta"]["intent"] == "disease_info"


def test_red_flag_during_flow():
    s = session_store.get_session("test3")
    s.clear()
    process_message("I have headache", session=s)
    r2 = process_message("now chest pain ho raha hai", session=s)
    assert r2["meta"]["intent"] == "emergency"


def test_greeting_template_fallback():
    s = session_store.get_session("test4")
    s.clear()
    r = process_message("hello", session=s)
    assert r["meta"]["intent"] == "greeting"
    assert r["text"]


def test_unknown_falls_back_to_template():
    s = session_store.get_session("test5")
    s.clear()
    r = process_message("zxcv qwerty asdf", session=s)
    assert r["text"]
