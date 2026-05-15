import json


# LOAD SHL CATALOG

with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_assessments(query, top_k=5):

    query = query.lower().strip()

    scored_results = []

    for item in catalog:

        name = item.get("name", "")
        test_type = item.get("test_type", "")
        description = item.get("description", "")

        searchable_text = (
            f"{name} "
            f"{test_type} "
            f"{description}"
        ).lower()

        score = 0

        # SIMPLE KEYWORD MATCHING

        for word in query.split():

            if word in searchable_text:
                score += 1

        # EXTRA BOOSTS

        if "java" in query and (
            "technical" in test_type.lower()
            or "developer" in searchable_text
        ):
            score += 3

        if "personality" in query and (
            "personality" in test_type.lower()
        ):
            score += 5

        if "communication" in query and (
            "communication" in searchable_text
            or "behavioral" in test_type.lower()
        ):
            score += 4

        if "leadership" in query and (
            "leadership" in searchable_text
            or "behavioral" in test_type.lower()
        ):
            score += 4

        if "cognitive" in query and (
            "cognitive" in test_type.lower()
        ):
            score += 4

        if score > 0:

            scored_results.append({
                "score": score,
                "data": item
            })

    # SORT BY SCORE

    scored_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # REMOVE DUPLICATES

    unique_results = []

    seen = set()

    for result in scored_results:

        item = result["data"]

        name = item.get("name")

        if name not in seen:

            seen.add(name)

            unique_results.append(item)

    return unique_results[:top_k]