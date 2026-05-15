import json
import pickle
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

print("Loading embedding model...")

model = SentenceTransformer(
    MODEL_NAME
)


with open(
    "data/shl_catalog.json",
    "r",
    encoding="utf-8"
) as file:

    catalog = json.load(
        file
    )


documents=[]

for item in catalog:

    text=f"""
    Name:{item['name']}
    Description:{item['description']}
    Test Type:{item['test_type']}
    """

    documents.append(
        text
    )


print(
    f"Creating embeddings for {len(documents)} assessments..."
)


vectors=model.encode(
    documents,
    convert_to_numpy=True
)


dimension=vectors.shape[1]


index=faiss.IndexFlatL2(
    dimension
)


index.add(
    vectors.astype(
        np.float32
    )
)


os.makedirs(
    "embeddings",
    exist_ok=True
)


faiss.write_index(
    index,
    "embeddings/faiss.index"
)


with open(
    "embeddings/metadata.pkl",
    "wb"
) as file:

    pickle.dump(
        catalog,
        file
    )


print(
    "Embeddings created successfully"
)