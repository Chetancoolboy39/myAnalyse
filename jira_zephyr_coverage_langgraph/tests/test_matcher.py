import pytest
from app.embeddings.matcher import EmbeddingMatcher

class DummyMatcher(EmbeddingMatcher):
    def _embed(self, texts):
        import numpy as np
        return np.random.rand(len(texts), self.dim)

def test_dummy_coverage():
    matcher = DummyMatcher()
    reqs = [{"id": "R1", "summary": "Login must validate user"}]
    tests = [{"id": "T1", "name": "Test login validation"}]
    results = matcher.check_coverage(reqs, tests)
    assert "requirement" in results[0]
    assert "matched_test" in results[0]
    assert "similarity" in results[0]
