from rag_chunk_eval.chunkers import fixed_size, sentence, paragraph, recursive
from rag_chunk_eval.eval import evaluate, compare, best_strategy, token_estimate

TEXT = "Artificial intelligence is transforming the world.\n\nMachine learning models can now understand language, generate code, and reason about complex problems.\n\nThe key breakthrough has been transformer architectures and large-scale pretraining.\n\nHowever, challenges remain: hallucination, bias, and the high cost of inference at scale."


class TestChunkers:
    def test_fixed_size(self):
        chunks = fixed_size(TEXT, size=200, overlap=20)
        assert len(chunks) >= 1
        for c in chunks:
            assert len(c.text) <= 200 + 20

    def test_sentence(self):
        chunks = sentence(TEXT, max_sentences=2)
        assert len(chunks) >= 1

    def test_paragraph(self):
        chunks = paragraph(TEXT)
        assert len(chunks) >= 2  # has multiple paragraphs

    def test_recursive(self):
        chunks = recursive(TEXT, target_size=300)
        assert len(chunks) >= 1


class TestEval:
    def test_evaluate_returns_score(self):
        chunks = fixed_size(TEXT, size=200)
        result = evaluate(chunks, "fixed_size")
        assert 0 <= result.score <= 1
        assert result.chunk_count > 0

    def test_compare_returns_results(self):
        results = compare(TEXT)
        assert len(results) == 4  # 4 strategies
        # Best strategy should have highest score
        for i in range(1, len(results)):
            assert results[i - 1].score >= results[i].score

    def test_empty_text(self):
        assert evaluate(fixed_size(""), "fixed").chunk_count == 0


class TestBestStrategy:
    def test_returns_valid_strategy(self):
        name, result = best_strategy(TEXT)
        assert name in {"fixed_size", "sentence", "paragraph", "recursive"}
        assert 0 <= result.score <= 1

    def test_matches_top_of_compare(self):
        name, result = best_strategy(TEXT)
        top = compare(TEXT)[0]
        assert result.score == top.score
        assert name == top.strategy

    def test_empty_text(self):
        name, result = best_strategy("")
        assert name in {"fixed_size", "sentence", "paragraph", "recursive"}
        assert result.score == 0


class TestTokenEstimate:
    def test_empty(self):
        assert token_estimate("") == 0

    def test_short_string(self):
        assert token_estimate("abcd") == 1

    def test_monotonic(self):
        assert token_estimate("a" * 400) >= token_estimate("a" * 200)