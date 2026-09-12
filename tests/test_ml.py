import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core import kb, retriever
from app.factcheck import verifier

kb.load()
verifier._ensure_index()
retriever._ensure_index()


def test_factcheck_myth():
    result = verifier.verify_claim("Vaccines cause autism in children")
    assert result["verdict"] == "MYTH"


def test_factcheck_true():
    result = verifier.verify_claim("ORS is the right first treatment for diarrhoea")
    assert result["verdict"] == "TRUE"


def test_factcheck_cancer_cure_is_myth():
    result = verifier.verify_claim("Turmeric cures cancer")
    assert result["verdict"] == "MYTH"


def test_factcheck_partly_true():
    result = verifier.verify_claim("Drinking haldi doodh relieves cold symptoms")
    assert result["verdict"] == "PARTLY_TRUE"


def test_factcheck_unverifiable():
    result = verifier.verify_claim("A new miracle drink cures every disease known to science")
    assert result["verdict"] == "UNVERIFIABLE"


def test_factcheck_hindi_claim():
    result = verifier.verify_claim("मोबाइल फोन से ब्रेन कैंसर होता है")
    assert result["verdict"] == "MYTH"


def test_factcheck_confidence_bounds():
    result = verifier.verify_claim("Vaccines cause autism in children")
    assert 0 < result["confidence"] <= 99


def test_retrieval_disease():
    results = retriever.retrieve("What are the symptoms of dengue?")
    assert results[0]["type"] == "disease"
    assert results[0]["id"] == "dengue"


def test_retrieval_faq():
    results = retriever.retrieve("how to prepare ors at home")
    assert results[0]["type"] == "faq"
    assert results[0]["id"] == "ors_preparation"
