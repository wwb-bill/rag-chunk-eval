"""Evaluate chunking strategies."""

from dataclasses import dataclass
from .chunkers import Chunk


@dataclass
class EvalResult:
    strategy: str
    chunk_count: int
    avg_chunk_size: float
    size_variance: float
    score: float  # 0-1 overall score


def _avg_size(chunks: list[Chunk]) -> float:
    return sum(len(c.text) for c in chunks) / len(chunks) if chunks else 0


def _size_variance(chunks: list[Chunk]) -> float:
    avg = _avg_size(chunks)
    if avg == 0:
        return 0
    return sum((len(c.text) - avg) ** 2 for c in chunks) / len(chunks)


def _overlap_score(chunks: list[Chunk]) -> float:
    """How much content is duplicated across chunks (0=perfect, 1=all dup)."""
    if len(chunks) < 2:
        return 1.0
    # Simple: check if chunk starts before previous chunk ends
    overlap_count = 0
    for i in range(1, len(chunks)):
        if chunks[i].start_char < chunks[i - 1].end_char:
            overlap_count += 1
    return 1.0 - (overlap_count / (len(chunks) - 1))


def evaluate(chunks: list[Chunk], strategy_name: str) -> EvalResult:
    avg = _avg_size(chunks)
    var = _size_variance(chunks)
    overlap = _overlap_score(chunks)
    # Higher score = better (penalize high variance, reward coverage)
    coverage = sum(len(c.text) for c in chunks)
    score = min(1.0, (coverage / max(1, chunks[-1].end_char if chunks else 1)) * overlap * (1.0 - min(var / (avg * avg + 1), 0.5)))

    return EvalResult(
        strategy=strategy_name,
        chunk_count=len(chunks),
        avg_chunk_size=round(avg, 1),
        size_variance=round(var, 1),
        score=round(score, 4),
    )


def compare(text: str) -> list[EvalResult]:
    """Compare all chunking strategies on a text."""
    from .chunkers import fixed_size, sentence, paragraph, recursive

    results = []
    for name, fn in [("fixed_size", fixed_size), ("sentence", sentence), ("paragraph", paragraph), ("recursive", recursive)]:
        chunks = fn(text)
        results.append(evaluate(chunks, name))
    results.sort(key=lambda r: r.score, reverse=True)
    return results


def best_strategy(text: str) -> tuple[str, EvalResult]:
    """Return (strategy_name, result) for the highest-scoring strategy on a text."""
    results = compare(text)
    if not results:
        empty = EvalResult(strategy="", chunk_count=0, avg_chunk_size=0.0, size_variance=0.0, score=0.0)
        return "", empty
    return results[0].strategy, results[0]


def token_estimate(text: str) -> int:
    """Rough token estimate (chars / 4 heuristic) for chunk-budget planning."""
    return (len(text) + 3) // 4