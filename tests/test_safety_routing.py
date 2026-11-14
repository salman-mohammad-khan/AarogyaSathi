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
