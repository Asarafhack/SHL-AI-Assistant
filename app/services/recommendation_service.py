import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


model=SentenceTransformer(
    "all-MiniLM-L6-v2"
)

catalog=json.load(
    open(
        "data/shl_catalog.json",
        encoding="utf-8"
    )
)

index=faiss.read_index(
    "embeddings/faiss.index"
)


def rerank(results,query):

    query=query.lower()

    scored=[]

    for item in results:

        score=0

        text=(

            item.get(
                "name",""
            )+" "+

            item.get(
                "description",""
            )+" "+

            " ".join(
                item.get(
                    "keys",[]
                )
            )

        ).lower()


        keywords=query.split()

        for word in keywords:

            if word in text:
                score+=2


        if "java" in query:

            if "java" in text:
                score+=10

            if "automata" in text:
                score+=5


        if "stakeholder" in query:

            if "communication" in text:
                score+=8


        if "personality" in query:

            if "personality" in text:
                score+=8


        scored.append(
            (
                score,
                item
            )
        )


    scored.sort(
        reverse=True,
        key=lambda x:x[0]
    )

    return [

        x[1]

        for x in scored
    ]


def get_recommendations(
    query,
    top_k=5
):

    embedding=model.encode(
        [query]
    )

    D,I=index.search(
        np.array(
            embedding,
            dtype=np.float32
        ),
        20
    )

    retrieved=[]

    for idx in I[0]:

        if idx<len(catalog):

            retrieved.append(
                catalog[idx]
            )


    ranked=rerank(
        retrieved,
        query
    )


    results=[]

    for x in ranked[:top_k]:

        results.append({

    "name": x["name"],

    "url": x["url"],

    "test_type": x.get(
        "test_type",
        "General"
    )

})


    return results