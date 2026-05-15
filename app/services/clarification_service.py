def needs_clarification(message: str):

    message = message.lower().strip()

    vague_queries = [

        "assessment",
        "test",
        "need assessment",
        "need a test",
        "i need an assessment",
        "recommend assessment"
    ]

    if message in vague_queries:
        return True

    return False


def generate_clarification():

    return (
        "Can you share the role seniority, "
        "required technical skills, or whether "
        "you also need personality or behavioral assessments?"
    )