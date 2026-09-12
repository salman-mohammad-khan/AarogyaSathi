import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.surveillance import syndromic
from app.factcheck import verifier


def test_rating_mapping():
    assert verifier._rating_to_verdict("False") == "MYTH"
    assert verifier._rating_to_verdict("Mostly False") == "MYTH"
    assert verifier._rating_to_verdict("True") == "TRUE"
    assert verifier._rating_to_verdict("Mostly True") == "TRUE"
    assert verifier._rating_to_verdict("Half True") == "PARTLY_TRUE"
    assert verifier._rating_to_verdict("Misleading") == "PARTLY_TRUE"
    assert verifier._rating_to_verdict("Satire") == "UNVERIFIABLE"


def test_spike_detection_creates_alert():
    syndromic.clear_all()
    day = 24 * 3600
    now = time.time()
    with syndromic._lock:
        conn = syndromic._conn()
        for i in range(2):
            ts = now - (i + 3) * day
            conn.execute("INSERT INTO events (pincode, symptom, lang, ts) VALUES ('999999', 'fever', 'en', ?)", (ts,))
        for i in range(8):
            ts = now - i * 3600
            conn.execute("INSERT INTO events (pincode, symptom, lang, ts) VALUES ('999999', 'fever', 'en', ?)", (ts,))
        conn.commit()
        conn.close()
    alerts = syndromic.run_detection("999999")
    assert len(alerts) == 1
    assert alerts[0]["symptom"] == "fever"
    assert alerts[0]["severity"] in ("medium", "high")
    again = syndromic.run_detection("999999")
    assert again == []
    active = syndromic.active_alerts()
    assert len(active) >= 1
    syndromic.clear_all()


def test_stats_shape():
    syndromic.clear_all()
    syndromic.record_message("123456", "symptom_check", "en", None)
    stats = syndromic.stats()
    assert "messages_24h" in stats
    assert stats["messages_24h"] >= 1
    syndromic.clear_all()


def test_live_lookup_disabled_without_key():
    assert verifier._live_lookup("some unknown claim about health", "en") is None
