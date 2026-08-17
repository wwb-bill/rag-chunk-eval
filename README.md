# rag-chunk-eval

Evaluate chunking strategies for RAG pipelines. Zero-dependency Python.

## Features

- **4 chunkers:** `fixed_size`, `sentence`, `paragraph`, `recursive`
- **Scoring engine:** size variance, overlap penalty, coverage → 0-1 score
- **`compare(text)`** — rank all strategies on a document
- **`best_strategy(text)`** — pick the top strategy automatically
- **`token_estimate(text)`** — rough char/4 token count for budget planning

## Install

```bash
pip install rag-chunk-eval
```

## Usage

```python
from rag_chunk_eval import compare, best_strategy
from rag_chunk_eval.chunkers import recursive

results = compare(document_text)          # [EvalResult(strategy="sentence", score=0.95), ...]
name, top = best_strategy(document_text)  # ("sentence", EvalResult(...))

chunks = recursive(document_text, target_size=400)
```

## API

| Function | Description |
|----------|-------------|
| `fixed_size(text, size=500, overlap=50)` | Fixed-size windows with overlap |
| `sentence(text, max_sentences=5)` | Group sentences into chunks |
| `paragraph(text)` | Split on blank-line paragraphs |
| `recursive(text, target_size=500)` | Recursive separator splitting |
| `compare(text)` | Rank all strategies by score |
| `best_strategy(text)` | (name, result) of the top strategy |
| `token_estimate(text)` | Rough token count (len/4) |

## Test

```bash
pip install -e ".[dev]"
pytest
```

MIT