OFF_TOPIC_KEYWORDS = [

    "bitcoin",
    "crypto",
    "ethereum",
    "weather",
    "football",
    "movie",
    "politics",
    "investment",
    "stock market",
    "medical advice",
    "relationship"
]


def is_off_topic(message: str):

    message = message.lower()

    for keyword in OFF_TOPIC_KEYWORDS:

        if keyword in message:
            return True

    return False