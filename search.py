import json
import faiss
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.read_index("catalog.index")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_catalog(query, top_k=5):
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for idx in indices[0]:
        results.append(catalog[idx])

    return results