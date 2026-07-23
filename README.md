# rag-chunk-eval

Evaluate chunking strategies for RAG. 4 strategies, scoring engine.

```python
from rag_chunk_eval import compare
results = compare(document_text)  # [EvalResult(strategy="sentence", score=0.95), ...]
```

MIT
