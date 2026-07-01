import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("Loading catalog...")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = [item["name"] for item in catalog]

print("Building TF-IDF vectors...")

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(texts)


def search_catalog(query, top_k=5):
    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    top_indices = similarities.argsort()[-top_k:][::-1]

    results = []

    for idx in top_indices:
        results.append(catalog[idx])

    return results