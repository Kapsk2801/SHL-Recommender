import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rapidfuzz import process, fuzz

print("Loading catalog...")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = [item["name"] for item in catalog]

print("Building TF-IDF vectors...")

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)


def fuzzy_search(query, top_k=5):
    matches = process.extract(
        query,
        texts,
        scorer=fuzz.partial_ratio,
        limit=top_k
    )

    results = []

    for match in matches:
        matched_text = match[0]

        for item in catalog:
            if item["name"] == matched_text:
                results.append(item)
                break

    return results


def search_catalog(query, top_k=5):
    # TF-IDF search
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    top_indices = similarities.argsort()[-top_k:][::-1]

    tfidf_results = [catalog[idx] for idx in top_indices]

    # If weak similarity, fallback to fuzzy matching
    if similarities[top_indices[0]] < 0.15:
        return fuzzy_search(query, top_k)

    return tfidf_results