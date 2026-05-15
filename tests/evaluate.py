from app.retrieval.vector_search import (
    search_assessments
)

queries = [

    "Hiring Java developer",

    "Need stakeholder communication assessment",

    "Need personality assessment",

    "Frontend engineer",

    "Leadership hiring"
]


for query in queries:

    print("\n===================")
    print("QUERY:", query)

    results = search_assessments(
        query,
        top_k=3
    )

    for item in results:

        print(
            "-",
            item["name"]
        )