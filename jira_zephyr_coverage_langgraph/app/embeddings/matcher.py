from typing import List, Dict
from openai import OpenAI
import faiss
import numpy as np
import os

class EmbeddingMatcher:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.dim = 1536
        self.index = faiss.IndexFlatL2(self.dim)

    def _embed(self, texts: List[str]) -> np.ndarray:
        embeddings = self.client.embeddings.create(model="text-embedding-ada-002", input=texts)
        return np.array([e.embedding for e in embeddings.data])

    def check_coverage(self, requirements: List[Dict], tests: List[Dict]) -> List[Dict]:
        req_texts = [r['summary'] for r in requirements]
        test_texts = [t['name'] for t in tests]

        req_vecs = self._embed(req_texts)
        test_vecs = self._embed(test_texts)

        self.index.add(test_vecs)
        results = []

        for i, r in enumerate(requirements):
            D, I = self.index.search(np.array([req_vecs[i]]), 1)
            matched_test = tests[I[0][0]]
            similarity = float(1 / (1 + D[0][0]))
            results.append({
                "requirement": r['id'],
                "matched_test": matched_test['id'],
                "similarity": similarity,
                "covered": similarity > 0.75
            })

        return results
