import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


model = None
index = None
metadata = None


def load_resources():

    global model
    global index
    global metadata

    if model is None:

        print("Loading embedding model...")

        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )

    if index is None:

        print("Loading FAISS index...")

        index = faiss.read_index(
            "embeddings/faiss.index"
        )

    if metadata is None:

        print("Loading metadata...")

        with open(
            "embeddings/metadata.pkl",
            "rb"
        ) as f:

            metadata = pickle.load(f)


def search_assessments(
    query,
    top_k=5
):

    load_resources()

    query_embedding = model.encode(
        [query]
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for idx in indices[0]:

        if (
            idx >= 0
            and idx < len(metadata)
        ):

            results.append(
                metadata[idx]
            )

    return results