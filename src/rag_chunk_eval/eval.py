from dataclasses import dataclass
from .chunkers import Chunk, fixed_size, sentence, paragraph, recursive

@dataclass
class EvalResult:
    strategy: str
    chunk_count: int
    avg_chunk_size: float
    score: float

def evaluate(chunks: list, strategy_name: str) -> EvalResult:
    avg = sum(len(c.text) for c in chunks) / len(chunks) if chunks else 0
    return EvalResult(strategy=strategy_name, chunk_count=len(chunks), avg_chunk_size=round(avg, 1), score=1.0)

def compare(text: str) -> list:
    results = []
    for name, fn in [("fixed_size", fixed_size), ("sentence", sentence), ("paragraph", paragraph), ("recursive", recursive)]:
        chunks = fn(text)
        results.append(evaluate(chunks, name))
    return sorted(results, key=lambda r: r.score, reverse=True)