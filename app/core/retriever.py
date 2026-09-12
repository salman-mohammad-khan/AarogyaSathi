import numpy as np

from app.config import RETRIEVAL_SIM_THRESHOLD, MAX_RETRIEVED
from app.core import embeddings, kb

_index = None


def _build_corpus():
    entries = []
    texts = []
    for d in kb.diseases():
        en_name = d["names"].get("en", [d["id"]])[0]
        hi_name = d["names"].get("hi", [en_name])[0]
        parts = []
        all_names = []
        for names in d["names"].values():
            all_names.extend(names)
        parts.append(" | ".join(all_names))
        if d.get("hinglish"):
            parts.append(d["hinglish"])
        parts.append(f"What is {en_name}? {en_name} symptoms, causes, prevention, treatment")
        parts.append(f"{hi_name} kya hai? {hi_name} ke lakshan, kaaran, bachav, ilaaj")
        if d.get("summary", {}).get("en"):
            parts.append(d["summary"]["en"][:180])
        texts.append(" | ".join(parts)[:600])
        entries.append({"type": "disease", "id": d["id"]})
    for f in kb.faqs():
        parts = []
        for lang in ["en", "hi", "hinglish"]:
            if lang in f.get("q", {}):
                parts.append(f["q"][lang])
        texts.append(" | ".join(parts))
        entries.append({"type": "faq", "id": f["id"]})
    return entries, texts


def _ensure_index():
    global _index
    if _index is not None:
        return _index
    entries, texts = _build_corpus()
    matrix = embeddings.embed_with_cache("kb_corpus", texts)
    _index = {"entries": entries, "texts": texts, "matrix": matrix}
    return _index


def retrieve(query, top_k=MAX_RETRIEVED, threshold=RETRIEVAL_SIM_THRESHOLD):
    index = _ensure_index()
    if not query.strip():
        return []
    qv = embeddings.embed_texts([query])[0]
    sims = embeddings.cosine_similarity(qv, index["matrix"])
    query_words = [w for w in query.lower().split() if len(w) > 2]
    scores = []
    for i, sim in enumerate(sims):
        score = float(sim)
        if query_words:
            entry_text = index["texts"][i].lower()
            matched = sum(1 for w in query_words if w in entry_text)
            lexical_ratio = matched / len(query_words)
            score += 0.22 * lexical_ratio
        scores.append(score)
    order = np.argsort(scores)[::-1]
    results = []
    seen = set()
    for i in order:
        if scores[i] < threshold:
            break
        key = (index["entries"][i]["type"], index["entries"][i]["id"])
        if key in seen:
            continue
        seen.add(key)
        results.append(
            {
                "type": index["entries"][i]["type"],
                "id": index["entries"][i]["id"],
                "score": float(scores[i]),
                "similarity": float(sims[i]),
            }
        )
        if len(results) >= top_k:
            break
    return results
