"""Regression tests for safety ordering and whole-word entity matching.

Each test pins a bug found in a code audit of the router:
  * fact-check triggers were evaluated before the emergency check,
  * short aliases matched inside other words ("tb" in "outbreak", "fits" in "benefits"),
  * self-harm phrases were not recognised,
  * "N years" was read as a child's age even when it was a duration.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core import entities, generator, intent, kb, safety
from app.core import router
from app.core import session as session_store

kb.load()
intent.load()
generator._availability = False  # templates only, no LLM


@pytest.fixture
def fact_check_spy(monkeypatch):
    """Replace the fact-checker with a stub and record every claim it is asked to verify."""
    calls = []

    def fake_verify(text, lang):
        calls.append(text)
        return {"verdict": "MYTH"}

    monkeypatch.setattr(router.verifier, "verify_claim", fake_verify)
    monkeypatch.setattr(router.verifier, "format_verdict", lambda result, lang: "FACT-CHECK VERDICT")
    return calls


def _fresh_session(name):
    s = session_store.get_session(name)
    s.clear()
    return s


# --- whole-word matching ---------------------------------------------------------------------------------

def test_disease_alias_not_matched_inside_other_words():
    assert entities.find_disease("any outbreak near 110001") is None
    assert entities.find_disease("she has a lot of influence") is None
    assert entities.find_disease("look at this") is None


def test_short_disease_aliases_still_match_as_words():
    assert entities.find_disease("tb symptoms") == "tuberculosis"
    assert entities.find_disease("What is TB?") == "tuberculosis"
    assert entities.find_disease("flu symptoms") == "influenza"
    assert entities.find_disease("loo se bachne ke tarike") == "heatstroke"


def test_devanagari_aliases():
    assert entities.find_disease("टीबी क्या है") == "tuberculosis"
    assert entities.find_disease("लू से बचाव") == "heatstroke"
    assert entities.find_disease("बालू पर चलना") is None  # "लू" inside another word


def test_plural_and_verb_forms_still_match():
    syms = entities.find_symptoms("I get headaches and keep coughing")
    assert "headache" in syms
    assert "cough" in syms


def test_negation_still_respected():
    syms = entities.find_symptoms("headache and no fever")
    assert "fever" not in syms
    assert "headache" in syms


# --- red flags -------------------------------------------------------------------------------------------

@pytest.mark.parametrize("text", [
    "health benefits of walking daily",
    "fitness tips for beginners",
    "how to prevent food poisoning",
    "heatstroke prevention tips",
    "the toast was burnt",
    "is that snake poisonous",
])
def test_information_questions_are_not_emergencies(text):
    assert safety.check_red_flags(text) == []


@pytest.mark.parametrize("text,flag", [
    ("my child drank poison", "poison"),
    ("he was poisoned", "poison"),
    ("mere papa ko chest pain ho raha hai", "chest_pain"),
    ("saap ne kaat liya mujhe", "snake_bite"),
    ("she is having fits", "seizure"),
    ("severe burn on his arm", "severe_burn"),
    ("face drooping and slurred speech", "stroke"),
])
def test_real_emergencies_still_detected(text, flag):
    assert flag in safety.check_red_flags(text)


@pytest.mark.parametrize("text", [
    "I want to end my life",
    "i dont want to live anymore",
    "I feel like I want to die",
    "mujhe marna chahta hoon",
    "मैं मरना चाहता हूँ",
    "thinking about suicide",
])
def test_self_harm_phrases_detected(text):
    assert safety.is_self_harm(safety.check_red_flags(text))


# --- routing order ---------------------------------------------------------------------------------------

def test_emergency_beats_fact_check_trigger(fact_check_spy):
    s = _fresh_session("sr_emergency_first")
    r = router.process_message("check this: my father has chest pain and cannot breathe", session=s)
    assert r["meta"]["intent"] == "emergency"
    assert fact_check_spy == []  # the fact-checker must never run
    assert "108" in r["text"]
    assert "send that claim again" in r["text"]  # tells the user how to fact-check instead


def test_plain_fact_check_still_runs(fact_check_spy):
    s = _fresh_session("sr_factcheck")
    r = router.process_message("fact check: drinking hot water every hour kills the covid virus", session=s)
    assert r["meta"]["intent"] == "fact_check"
    assert len(fact_check_spy) == 1


def test_self_harm_gets_mental_health_helpline(fact_check_spy):
    s = _fresh_session("sr_self_harm")
    r = router.process_message("I want to end my life", session=s)
    assert r["meta"]["intent"] == "emergency"
    assert "14416" in r["text"]
    assert "112" in r["text"]
    assert fact_check_spy == []


def test_outbreak_query_not_hijacked_by_tb_alias():
    s = _fresh_session("sr_outbreak")
    r = router.process_message("any outbreak near 110001", pincode="110001", session=s)
    assert r["meta"].get("disease") != "tuberculosis"


# --- vaccination age vs duration -------------------------------------------------------------------------

def test_duration_is_not_a_vaccination_age():
    assert router._age_to_milestones("I have had this cough for 2 years") is None
    assert router._age_to_milestones("my baby has had fever for 2 months") is None
    assert router._age_to_milestones("knee pain since 3 years") is None


def test_real_ages_still_map_to_milestones():
    assert router._age_to_milestones("my baby is 6 weeks old") == "6_weeks"
    assert router._age_to_milestones("which vaccine at 14 weeks") == "14_weeks"
    assert router._age_to_milestones("meri beti 10 saal ki hai kaun sa tika") == "10_years"
    assert router._age_to_milestones("I am pregnant") == "pregnancy"


# --- natural phrasings, Hinglish and language misdetection of emergencies --------------------------------
# Phrases added after probing the live demo: the emergency path missed natural English ("a snake just bit my
# brother") and romanised Hindi ("seene mein dard ho raha hai"), answered one romanised message in Kannada, and
# appended a snake-bite tip to every emergency reply, even chest pain.

NATURAL_EMERGENCIES = [
    ("A snake just bit my brother", "snake_bite"),
    ("my brother was bitten by a snake", "snake_bite"),
    ("a cobra bit my father in the field", "snake_bite"),
    ("seene mein dard ho raha hai", "chest_pain"),
    ("sine me bahut dard hai", "chest_pain"),
    ("mere bhai ko saap ne kaat liya hai", "snake_bite"),
    ("sanp ne kata mujhe", "snake_bite"),
    ("I have a sharp pain in my chest", "chest_pain"),
    ("my father says his chest hurts and feels tight", "chest_pain"),
    ("a dog bit my son this morning", "rabid_animal"),
    ("kutte ne kaat liya", "rabid_animal"),
    ("सीने में तेज दर्द हो रहा है", "chest_pain"),
    ("मेरे भाई को साँप ने काट लिया है", "snake_bite"),
]


@pytest.mark.parametrize("text,flag", NATURAL_EMERGENCIES)
def test_natural_phrasings_are_red_flags(text, flag):
    assert flag in safety.check_red_flags(text)


@pytest.mark.parametrize("text,flag", NATURAL_EMERGENCIES)
def test_natural_phrasings_route_to_emergency_reply(text, flag, fact_check_spy):
    s = _fresh_session("sr_natural_" + str(abs(hash(text))))
    r = router.process_message(text, session=s)
    assert r["meta"]["intent"] == "emergency"
    assert flag in r["meta"]["red_flags"]
    assert "108" in r["text"] and "112" in r["text"]
    assert fact_check_spy == []


@pytest.mark.parametrize("text", [
    "is that snake poisonous",
    "snake sightings in my village this year",
    "do snakes live near water",
    "my chest x-ray report is ready",
    "chest day workout plan",
    "the python script bit me with a bug",
    "dog food brands in India",
    "a monkey sat on the roof",
])
def test_nearby_wording_without_an_emergency_stays_quiet(text):
    assert safety.check_red_flags(text) == []


@pytest.mark.parametrize("wrong_lang", ["kn", "ta", "te", "bn", "mr", "ml", "gu", "pa", "or", "ur"])
def test_romanised_hindi_emergency_survives_language_misdetection(monkeypatch, wrong_lang):
    # fastText labelled "mere bhai ko saap ne kaat liya hai" as Kannada on the demo VM.
    monkeypatch.setattr(router.language, "detect_language", lambda text: wrong_lang)
    s = _fresh_session("sr_misdetect_" + wrong_lang)
    r = router.process_message("mere bhai ko saap ne kaat liya hai", session=s)
    assert r["meta"]["intent"] == "emergency"
    assert r["meta"]["lang"] == "hi"
    assert "साँप" in r["text"] and "112" in r["text"]
    assert "ಸಹಾಯವಾಣಿ" not in r["text"]  # no Kannada helpline text


def test_romanised_english_emergency_misdetected_as_another_language_gets_english(monkeypatch):
    monkeypatch.setattr(router.language, "detect_language", lambda text: "kn")
    s = _fresh_session("sr_misdetect_en")
    r = router.process_message("A snake just bit my brother", session=s)
    assert r["meta"]["lang"] == "en"
    assert "National Health Helpline" in r["text"]


def test_romanised_hindi_chest_pain_with_wrong_label_gets_hindi(monkeypatch):
    monkeypatch.setattr(router.language, "detect_language", lambda text: "kn")
    s = _fresh_session("sr_misdetect_chest")
    r = router.process_message("seene mein dard ho raha hai", session=s)
    assert r["meta"]["lang"] == "hi"
    assert "112" in r["text"]


def test_emergency_language_keeps_script_based_detection():
    assert safety.emergency_language("மார்பு வலி உள்ளது", "ta") == "ta"
    assert safety.emergency_language("सीने में दर्द", "hi") == "hi"
    assert safety.emergency_language("I have chest pain", "en") == "en"
    assert safety.emergency_language("mere papa ko seene mein dard hai", "en") == "hi"
    assert safety.emergency_language("mere papa ko seene mein dard hai", "kn") == "hi"
    assert safety.emergency_language("help, chest pain", "kn") == "en"


def test_self_harm_reply_language_is_also_corrected(monkeypatch):
    monkeypatch.setattr(router.language, "detect_language", lambda text: "kn")
    s = _fresh_session("sr_misdetect_selfharm")
    r = router.process_message("mujhe marna chahta hoon", session=s)
    assert r["meta"]["lang"] == "hi"
    assert "14416" in r["text"]


# --- the snake-bite tip belongs only to snake bites ---------------------------------------------------------

@pytest.mark.parametrize("text", [
    "I have chest pain",
    "seene mein dard ho raha hai",
    "सीने में तेज दर्द हो रहा है",
    "he is unconscious and not responding",
    "my child drank poison",
])
def test_non_snake_emergencies_have_no_snake_bite_tip(text):
    s = _fresh_session("sr_no_snake_tip")
    r = router.process_message(text, session=s)
    assert r["meta"]["intent"] == "emergency"
    assert "snake" not in r["text"].lower()
    assert "साँप" not in r["text"]
    assert "108" in r["text"]


def test_snake_bite_keeps_its_first_aid_tip_before_the_helplines():
    en = safety.emergency_response("en", ["snake_bite"])
    assert "anti-venom" in en
    assert en.index("anti-venom") < en.index("National Health Helpline")
    hi = safety.emergency_response("hi", ["snake_bite"])
    assert "साँप" in hi
    # the generic template and the no-flag call carry no tip
    assert "snake" not in safety.emergency_response("en").lower()
    assert "snake" not in kb.msg("en", "emergency").lower()
    assert "साँप" not in kb.msg("hi", "emergency")


def test_languages_without_a_tip_text_get_the_plain_emergency_reply():
    assert safety.emergency_response("ta", ["snake_bite"]) == safety.emergency_response("ta")
