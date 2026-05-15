from retrieval.vector_search import search_assessments


def keyword_score(query,item):

    query_words=set(
        query.lower().split()
    )

    item_words=set(
        item["name"].lower().split()
    )

    overlap=len(
        query_words.intersection(
            item_words
        )
    )

    return overlap


def hybrid_search(
    query,
    top_k=5
):

    semantic_results=search_assessments(
        query,
        top_k=10
    )

    scored=[]

    for item in semantic_results:

        score=keyword_score(
            query,
            item
        )

        scored.append(
            (score,item)
        )

    scored=sorted(
        scored,
        reverse=True,
        key=lambda x:x[0]
    )

    return [

        item
        for score,item
        in scored[:top_k]
    ]