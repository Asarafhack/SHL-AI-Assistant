import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

index = faiss.read_index("embeddings/faiss.index")

texts = [
    f"{item['name']} {item['description']} {' '.join(item.get('skills', []))}"
    for item in catalog
]

def search_assessments(query, top_k=5):

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:

        if idx >= len(catalog):
            continue

        results.append(catalog[idx])

    return results