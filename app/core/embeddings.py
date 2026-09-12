import hashlib
import json
import os
import threading

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

from app.config import EMBEDDING_MODEL, EMBEDDING_CACHE_DIR

torch.set_num_threads(int(os.environ.get("EMBED_THREADS", "4")))

_tokenizer = None
_model = None
_lock = threading.Lock()


def _mean_pool(token_embeddings, attention_mask):
    mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    summed = torch.sum(token_embeddings * mask, dim=1)
    counts = torch.clamp(mask.sum(dim=1), min=1e-9)
    return summed / counts


def get_model():
    global _tokenizer, _model
    if _model is None:
        with _lock:
            if _model is None:
                try:
                    _tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL, local_files_only=True)
                    _model = AutoModel.from_pretrained(EMBEDDING_MODEL, local_files_only=True)
                except Exception:
                    _tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
                    _model = AutoModel.from_pretrained(EMBEDDING_MODEL)
                _model.eval()
    return _tokenizer, _model


def embed_texts(texts):
    tokenizer, model = get_model()
    if not texts:
        return np.zeros((0, 768), dtype=np.float32)
    all_vectors = []
    for i in range(0, len(texts), 32):
        batch = list(texts[i : i + 32])
        encoded = tokenizer(
            batch,
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="pt",
        )
        with torch.no_grad():
            out = model(**encoded)
        pooled = _mean_pool(out.last_hidden_state, encoded["attention_mask"])
        pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
        all_vectors.append(pooled.cpu().numpy().astype(np.float32))
    return np.vstack(all_vectors)


def _cache_key(prefix, items):
    payload = json.dumps(items, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()[:16]
    return EMBEDDING_CACHE_DIR / f"{prefix}_{digest}.npy"


def embed_with_cache(prefix, texts, force=False):
    key = _cache_key(prefix, texts)
    if not force and key.exists():
        return np.load(key)
    print(f"[embeddings] building cache for '{prefix}' ({len(texts)} entries)...", flush=True)
    vectors = embed_texts(texts)
    np.save(key, vectors)
    return vectors


def cosine_similarity(query_vector, corpus_matrix):
    if corpus_matrix.size == 0:
        return np.zeros(0, dtype=np.float32)
    query_vector = np.asarray(query_vector, dtype=np.float32)
    norms = np.linalg.norm(corpus_matrix, axis=1)
    denom = norms * np.linalg.norm(query_vector) + 1e-9
    return (corpus_matrix @ query_vector) / denom
