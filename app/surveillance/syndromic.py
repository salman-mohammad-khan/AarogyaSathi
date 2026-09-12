import sqlite3
import threading
import time
from pathlib import Path

from app.config import DATA_DIR

DB_PATH = DATA_DIR / "surveillance.db"
_lock = threading.Lock()

WINDOW_HOURS = 24
BASELINE_DAYS = 7
SPIKE_RATIO = 3.0
SPIKE_MIN_COUNT = 6
DEDUP_HOURS = 24


def _conn():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _lock:
        conn = _conn()
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pincode TEXT NOT NULL,
                symptom TEXT NOT NULL,
                lang TEXT,
                ts REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pincode TEXT,
                intent TEXT,
                lang TEXT,
                verdict TEXT,
                ts REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pincode TEXT NOT NULL,
                symptom TEXT NOT NULL,
                current_count INTEGER,
                baseline REAL,
                severity TEXT,
                ts REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_events_pin_sym_ts ON events(pincode, symptom, ts);
            CREATE INDEX IF NOT EXISTS idx_messages_ts ON messages(ts);
            """
        )
        conn.commit()
        conn.close()


def record_symptom_event(pincode, symptoms, lang):
    if not pincode or not symptoms:
        return
    now = time.time()
    with _lock:
        conn = _conn()
        conn.executemany(
            "INSERT INTO events (pincode, symptom, lang, ts) VALUES (?, ?, ?, ?)",
            [(str(pincode), s, lang, now) for s in symptoms],
        )
        conn.commit()
        conn.close()


def record_message(pincode, intent_name, lang, verdict=None):
    with _lock:
        conn = _conn()
        conn.execute(
            "INSERT INTO messages (pincode, intent, lang, verdict, ts) VALUES (?, ?, ?, ?, ?)",
            (str(pincode) if pincode else None, intent_name, lang, verdict, time.time()),
        )
        conn.commit()
        conn.close()


def _counts(conn, pincode, symptom, start, end):
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM events WHERE pincode=? AND symptom=? AND ts>=? AND ts<?",
        (pincode, symptom, start, end),
    ).fetchone()
    return row["c"]


def _recent_alert(conn, pincode, symptom, since):
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM alerts WHERE pincode=? AND symptom=? AND ts>=?",
        (pincode, symptom, since),
    ).fetchone()
    return row["c"] > 0


def check_pair(pincode, symptom):
    now = time.time()
    window_start = now - WINDOW_HOURS * 3600
    baseline_start = now - (BASELINE_DAYS + 1) * 24 * 3600
    baseline_end = window_start
    with _lock:
        conn = _conn()
        current = _counts(conn, pincode, symptom, window_start, now)
        total_older = _counts(conn, pincode, symptom, baseline_start, baseline_end)
        baseline = total_older / BASELINE_DAYS
        if _recent_alert(conn, pincode, symptom, now - DEDUP_HOURS * 3600):
            conn.close()
            return None
        severity = None
        if current >= SPIKE_MIN_COUNT:
            if baseline >= 1.0 and current >= SPIKE_RATIO * baseline:
                severity = "high" if current >= 5 * baseline else "medium"
            elif baseline < 1.0 and current >= SPIKE_MIN_COUNT:
                severity = "medium"
        if severity:
            conn.execute(
                "INSERT INTO alerts (pincode, symptom, current_count, baseline, severity, ts) VALUES (?, ?, ?, ?, ?, ?)",
                (pincode, symptom, current, round(baseline, 2), severity, now),
            )
            conn.commit()
            alert = {
                "pincode": pincode,
                "symptom": symptom,
                "current_count": current,
                "baseline": round(baseline, 2),
                "severity": severity,
                "ts": now,
            }
            conn.close()
            return alert
        conn.close()
        return None


def run_detection(pincode=None):
    with _lock:
        conn = _conn()
        if pincode:
            rows = conn.execute(
                "SELECT DISTINCT pincode, symptom FROM events WHERE pincode=? AND ts>=?",
                (str(pincode), time.time() - WINDOW_HOURS * 3600),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT DISTINCT pincode, symptom FROM events WHERE ts>=?",
                (time.time() - WINDOW_HOURS * 3600,),
            ).fetchall()
        pairs = [(r["pincode"], r["symptom"]) for r in rows]
        conn.close()
    new_alerts = []
    for pin, sym in pairs:
        alert = check_pair(pin, sym)
        if alert:
            new_alerts.append(alert)
    return new_alerts


def active_alerts():
    with _lock:
        conn = _conn()
        rows = conn.execute(
            "SELECT * FROM alerts ORDER BY ts DESC LIMIT 50"
        ).fetchall()
        conn.close()
    return [dict(r) for r in rows]


def stats():
    now = time.time()
    day = 24 * 3600
    with _lock:
        conn = _conn()
        def counts(sql, params):
            return {r["k"]: r["c"] for r in conn.execute(sql, params).fetchall()}

        intents_24h = counts(
            "SELECT intent AS k, COUNT(*) AS c FROM messages WHERE ts>=? GROUP BY intent",
            (now - day,),
        )
        intents_7d = counts(
            "SELECT intent AS k, COUNT(*) AS c FROM messages WHERE ts>=? GROUP BY intent",
            (now - 7 * day,),
        )
        verdicts = counts(
            "SELECT verdict AS k, COUNT(*) AS c FROM messages WHERE verdict IS NOT NULL AND ts>=? GROUP BY verdict",
            (now - 7 * day,),
        )
        langs = counts(
            "SELECT lang AS k, COUNT(*) AS c FROM messages WHERE ts>=? GROUP BY lang",
            (now - 7 * day,),
        )
        events_24h = conn.execute(
            "SELECT COUNT(*) AS c FROM events WHERE ts>=?", (now - day,)
        ).fetchone()["c"]
        alerts_7d = conn.execute(
            "SELECT COUNT(*) AS c FROM alerts WHERE ts>=?", (now - 7 * day,)
        ).fetchone()["c"]
        conn.close()
    return {
        "messages_24h": sum(intents_24h.values()),
        "messages_7d": sum(intents_7d.values()),
        "intents_24h": intents_24h,
        "intents_7d": intents_7d,
        "verdicts_7d": verdicts,
        "languages_7d": langs,
        "symptom_events_24h": events_24h,
        "alerts_7d": alerts_7d,
    }


def seed_demo():
    now = time.time()
    day = 24 * 3600
    with _lock:
        conn = _conn()
        conn.execute("DELETE FROM events WHERE pincode='110001'")
        conn.execute("DELETE FROM alerts WHERE pincode='110001'")
        for i in range(1, BASELINE_DAYS + 1):
            for sym, jitter in [("diarrhoea", 0.5), ("fever", 0.2)]:
                ts = now - i * day + jitter * day
                conn.execute(
                    "INSERT INTO events (pincode, symptom, lang, ts) VALUES (?, ?, 'en', ?)",
                    ("110001", sym, ts),
                )
        for i in range(12):
            ts = now - i * 3600 * 1.5
            conn.execute(
                "INSERT INTO events (pincode, symptom, lang, ts) VALUES (?, ?, 'en', ?)",
                ("110001", "diarrhoea", ts),
            )
        conn.commit()
        conn.close()
    return run_detection("110001")


def clear_all():
    with _lock:
        conn = _conn()
        conn.execute("DELETE FROM events")
        conn.execute("DELETE FROM messages")
        conn.execute("DELETE FROM alerts")
        conn.commit()
        conn.close()


init_db()
