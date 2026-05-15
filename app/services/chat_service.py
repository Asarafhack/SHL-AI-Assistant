from app.retrieval.vector_search import (
    search_assessments
)

from app.services.clarification_service import (
    needs_clarification,
    generate_clarification
)

from app.services.comparison_service import (
    compare_assessments
)

from app.guardrails.scope_checker import (
    is_off_topic
)


def process_chat(request):

    messages = request.messages

    latest = messages[-1].content

    latest_lower = latest.lower()


    # =========================
    # INJECTION DEFENSE
    # =========================

    blocked = [

        "ignore previous instructions",
        "system prompt",
        "reveal hidden prompt",
        "hack",
        "bypass",
        "legal advice",
        "medical advice",
        "jailbreak"
    ]

    for word in blocked:

        if word in latest_lower:

            return {

                "reply": "I only assist with SHL assessments.",

                "recommendations": [],

                "end_of_conversation": True
            }


    # =========================
    # OFF TOPIC DEFENSE
    # =========================

    if is_off_topic(latest):

        return {

            "reply": "I only discuss SHL assessments and hiring evaluations.",

            "recommendations": [],

            "end_of_conversation": True
        }


    # =========================
    # COMPARISON FLOW
    # =========================

    if (

        "compare" in latest_lower
        or "difference" in latest_lower
        or " vs " in latest_lower

    ):

        comparison = compare_assessments(
            latest
        )

        return {

            "reply": comparison,

            "recommendations": [],

            "end_of_conversation": False
        }


    # =========================
    # CLARIFICATION FLOW
    # ONLY FIRST MESSAGE
    # =========================

    if len(messages) == 1:

        if needs_clarification(latest):

            return {

                "reply": generate_clarification(),

                "recommendations": [],

                "end_of_conversation": False
            }


    # =========================
    # MULTI TURN REFINEMENT
    # =========================

    merged_query = " ".join(

        [m.content for m in messages]
    )


    # =========================
    # RETRIEVAL
    # =========================

    results = search_assessments(

        merged_query,
        top_k=5
    )


    # =========================
    # PERSONALITY REFINEMENT
    # =========================

    if "personality" in merged_query.lower():

        personality_results = []

        for item in results:

            if item["test_type"] in [

                "Personality",
                "Behavioral"
            ]:

                personality_results.append(
                    item
                )

        if personality_results:

            results = personality_results


    # =========================
    # FORMAT RESPONSE
    # =========================

    recommendations = []

    for item in results:

        recommendations.append({

            "name": item["name"],

            "url": item["url"],

            "test_type": item["test_type"]
        })


    return {

        "reply": "Here are recommended SHL assessments.",

        "recommendations": recommendations,

        "end_of_conversation": True
    }