from app.retrieval.vector_search import (
    search_assessments
)


def compare_assessments(query):

    query = query.lower()


    if "opq" in query and "gsa" in query:

        return (
            "OPQ32r focuses on workplace personality "
            "and behavioral traits, while GSA focuses "
            "on cognitive ability and reasoning skills."
        )


    results = search_assessments(
        query,
        top_k=2
    )


    if len(results) < 2:

        return (
            "Unable to compare the requested assessments."
        )


    first = results[0]
    second = results[1]


    return (

        f"{first['name']} focuses on "
        f"{first['test_type']} evaluation, while "

        f"{second['name']} focuses on "
        f"{second['test_type']} evaluation."
    )