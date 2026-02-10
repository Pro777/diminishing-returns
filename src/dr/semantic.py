from __future__ import annotations

import json
import os
import urllib.request
from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(frozen=True)
class EmbeddingConfig:
    url: str
    model: str
    timeout_s: float = 10.0


def embedding_config_from_env() -> Optional[EmbeddingConfig]:
    """Return an embedding config if DR_OLLAMA_URL is set.

    Environment variables:
    - DR_OLLAMA_URL: e.g. http://127.0.0.1:11434
    - DR_OLLAMA_EMBED_MODEL: e.g. nomic-embed-text (default)
    """

    url = os.environ.get("DR_OLLAMA_URL")
    if not url:
        return None
    model = os.environ.get("DR_OLLAMA_EMBED_MODEL") or "nomic-embed-text"
    timeout_s = float(os.environ.get("DR_OLLAMA_TIMEOUT_S") or "10")
    return EmbeddingConfig(url=url.rstrip("/"), model=model, timeout_s=timeout_s)


def cosine_similarity(a: List[float], b: List[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have same dimension")
    dot = 0.0
    na = 0.0
    nb = 0.0
    for x, y in zip(a, b):
        dot += x * y
        na += x * x
        nb += y * y
    if na == 0.0 and nb == 0.0:
        return 1.0
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / ((na**0.5) * (nb**0.5))


def mean_vector(vectors: Iterable[List[float]]) -> List[float]:
    vectors = list(vectors)
    if not vectors:
        raise ValueError("Cannot compute mean of empty vector list")
    dim = len(vectors[0])
    if any(len(v) != dim for v in vectors):
        raise ValueError("Vectors must have same dimension")

    out = [0.0] * dim
    for v in vectors:
        for i, x in enumerate(v):
            out[i] += float(x)
    n = float(len(vectors))
    return [x / n for x in out]


def embed_ollama(config: EmbeddingConfig, prompts: List[str]) -> List[List[float]]:
    """Embed prompts using Ollama's embeddings endpoint.

    Calls POST {url}/api/embeddings with JSON: {model, prompt}

    Notes:
    - We intentionally keep this stdlib-only to avoid extra deps.
    - This is best-effort; caller should handle exceptions.
    """

    out: List[List[float]] = []
    endpoint = f"{config.url}/api/embeddings"

    for prompt in prompts:
        payload = json.dumps({"model": config.model, "prompt": prompt}).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=config.timeout_s) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        emb = data.get("embedding")
        if not isinstance(emb, list) or not emb:
            raise ValueError("Ollama embeddings response missing 'embedding'")
        out.append([float(x) for x in emb])

    return out
