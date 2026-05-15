import json
import pickle
import os

import faiss
import numpy as np


index = None
metadata = None


def load_resources():

    global index
    global metadata

    if index is None:

        print("Loading FAISS index...")

        index_path = os.path.join(
            "embeddings",
            "faiss.index"
        )

        index = faiss.read_index(
            index_path
        )

    if metadata is None:

        print("Loading metadata...")

        metadata_path = os.path.join(
            "embeddings",
            "metadata.pkl"
        )

        with open(
            metadata_path,
            "rb"
        ) as f:

            metadata = pickle.load(f)


def simple_text_score(
    query,
    text
):

    query_words = set(
        query.lower().split()
    )

    text_words = set(
        text.lower().split()
    )

    common = query_words.intersection(
        text_words
    )

    return len(common)


def search_assessments(
    query,
    top_k=5
):

    load_resources()

    scored_results = []

    for item in metadata:

        searchable_text = " ".join([
            item.get("name", ""),
            item.get("description", ""),
            item.get("test_type", "")
        ])

        score = simple_text_score(
            query,
            searchable_text
        )

        scored_results.append(
            (score, item)
        )

    scored_results.sort(
        key=lambda x: x[0],
        reverse=True
    )

    results = []

    for score, item in scored_results[:top_k]:

        if score > 0:

            results.append(item)

    return results