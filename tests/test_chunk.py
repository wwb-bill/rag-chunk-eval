from rag_chunk_eval import fixed_size, sentence, compare

class TestChunkers:
    def test_fixed_size(self):
        assert fixed_size("hello world", 3)[0].text == "hel"
    def test_sentence(self):
        chunks = sentence("Hi. Hello.")
        assert len(chunks) == 2
    def test_compare(self):
        results = compare("This is a test document. It has two sentences.")
        assert len(results) == 4
    def test_eval_score(self):
        from rag_chunk_eval import evaluate
        r = evaluate(fixed_size("test"), "fixed")
        assert r.score > 0