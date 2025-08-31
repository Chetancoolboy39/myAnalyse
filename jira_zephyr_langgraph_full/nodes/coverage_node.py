from langchain_openai import OpenAIEmbeddings
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

embeddings = OpenAIEmbeddings()

def embed(text):
    return np.array(embeddings.embed_query(text))

def compute_coverage(state: dict):
    requirements = state.get("requirements", [])
    tests = state.get("tests", [])
    coverage_results = []

    for req in requirements:
        req_vec = embed(req["description"])
        best_match = None
        best_score = 0.0
        for test in tests:
            test_vec = embed(test["description"])
            score = cosine_similarity([req_vec], [test_vec])[0][0]
            if score > best_score:
                best_score = score
                best_match = test
        coverage_results.append({
            "requirement": req,
            "matched_test": best_match,
            "similarity": best_score
        })

    state["coverage_results"] = coverage_results
    return state
