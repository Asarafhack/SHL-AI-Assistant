def needs_clarification(message: str):

    message = message.lower()

    vague_queries = [

        "assessment",
        "test",
        "developer",
        "engineer",
        "manager",
        "hiring"
    ]

    short_query = len(
        message.split()
    ) < 5

    for word in vague_queries:

        if word in message and short_query:
            return True

    return False


def generate_clarification():

    return (
        "Can you share the role seniority, "
        "required technical skills, or whether "
        "you also need personality or behavioral assessments?"
    )