import json
import re
import time
import urllib.parse
import xml.etree.ElementTree as ET

import httpx

from app.config import KB_DIR

_outbreaks = None
_pincodes = None
_news_cache = {}
NEWS_TTL = 15 * 60

PINCODE_RE = re.compile(r"\b[1-9]\d{5}\b")


def load():
    global _outbreaks, _pincodes
    if _outbreaks is None:
        with open(KB_DIR / "outbreaks.json", encoding="utf-8") as f:
            _outbreaks = json.load(f)
    if _pincodes is None:
        with open(KB_DIR / "pincodes.json", encoding="utf-8") as f:
            _pincodes = json.load(f)
    return _outbreaks, _pincodes


def extract_pincode(text):
    m = PINCODE_RE.search(text or "")
    return m.group(0) if m else None


def resolve_pincode(pincode):
    _, pc = load()
    pincode = str(pincode or "").strip()
    if len(pincode) < 6 or not pincode.isdigit():
        return None
    state = pc["circles"].get(pincode[:2])
    district = pc["districts"].get(pincode[:3])
    return {"pincode": pincode, "state": state, "district": district}


def match_outbreaks(pincode):
    out, _ = load()
    loc = resolve_pincode(pincode)
    if not loc:
        return [], None
    matched = []
    for o in out["outbreaks"]:
        if not o.get("active", True):
            continue
        if loc["state"] and loc["state"] in o.get("states", []):
            matched.append(o)
        elif loc["district"] and loc["district"] in o.get("districts", []):
            matched.append(o)
    return matched, loc


def active_outbreaks():
    out, _ = load()
    return [o for o in out["outbreaks"] if o.get("active", True)]


def search_news(query, limit=5):
    key = query.lower().strip()
    now = time.time()
    cached = _news_cache.get(key)
    if cached and now - cached["ts"] < NEWS_TTL:
        return cached["items"]
    items = []
    try:
        q = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={q}&hl=en-IN&gl=IN&ceid=IN:en"
        resp = httpx.get(url, timeout=10)
        root = ET.fromstring(resp.text)
        for it in root.iter("item"):
            title = (it.findtext("title") or "").strip()
            source = (it.findtext("source") or "").strip()
            pub = (it.findtext("pubDate") or "").strip()
            link = (it.findtext("link") or "").strip()
            if title:
                items.append({"title": title, "source": source, "date": pub, "link": link})
            if len(items) >= limit:
                break
    except Exception:
        items = []
    _news_cache[key] = {"ts": now, "items": items}
    return items
