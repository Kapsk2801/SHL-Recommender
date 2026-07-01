import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

print("Loading model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

texts = [item["name"] for item in catalog]

print("Generating embeddings...")

embeddings = model.encode(texts)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

faiss.write_index(index, "catalog.index")

print("Done. Index saved.")