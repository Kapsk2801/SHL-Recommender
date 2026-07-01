from search import search_catalog


OFFTOPIC_WORDS = [
    "salary",
    "legal",
    "contract",
    "notice period",
    "offer letter"
]

INJECTION_WORDS = [
    "ignore previous instructions",
    "forget everything",
    "system prompt",
    "bypass rules"
]


def get_latest_user_message(messages):
    """
    Get latest user message from conversation
    """
    for msg in reversed(messages):
        if msg["role"] == "user":
            return msg["content"]
    return ""


def extract_context(messages):
    """
    Combine all user messages for refinement handling
    """
    user_messages = []

    for msg in messages:
        if msg["role"] == "user":
            user_messages.append(msg["content"])

    return " ".join(user_messages)


def is_offtopic(text):
    """
    Detect off-topic hiring/legal queries
    """
    text = text.lower()
    return any(word in text for word in OFFTOPIC_WORDS)


def is_prompt_injection(text):
    """
    Detect prompt injection attempts
    """
    text = text.lower()
    return any(word in text for word in INJECTION_WORDS)


def is_vague(text):
    text = text.lower()

    vague_patterns = [
        "need assessment",
        "need an assessment",
        "looking for test",
        "want an assessment"
    ]

    # If enough hiring context exists, don't treat it as vague
    context_keywords = [
        "developer",
        "engineer",
        "python",
        "java",
        "backend",
        "frontend",
        "skills",
        "role"
    ]

    if any(word in text for word in context_keywords):
        return False

    return any(v == text.strip() for v in vague_patterns) or len(text.split()) < 3


def is_comparison(text):
    """
    Detect comparison requests
    """
    text = text.lower()

    comparison_keywords = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    return any(word in text for word in comparison_keywords)


def handle_comparison(text):
    """
    Compare two SHL assessments
    """
    results = search_catalog(text, top_k=2)

    if len(results) < 2:
        return {
            "reply": "I could not find enough SHL assessments to compare.",
            "recommendations": [],
            "end_of_conversation": False
        }

    return {
        "reply": f"{results[0]['name']} and {results[1]['name']} assess different dimensions. Please review both based on your hiring needs.",
        "recommendations": [
            {
                "name": r["name"],
                "url": r["url"],
                "test_type": "Unknown"
            }
            for r in results
        ],
        "end_of_conversation": False
    }


def handle_chat(messages):
    """
    Main agent logic
    """

    latest = get_latest_user_message(messages)
    full_context = extract_context(messages)

    # Prompt injection protection
    if is_prompt_injection(latest):
        return {
            "reply": "I can only assist with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Off-topic refusal
    if is_offtopic(latest):
        return {
            "reply": "I only assist with SHL assessments and cannot answer unrelated hiring or legal questions.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Comparison mode
    if is_comparison(latest):
        return handle_comparison(latest)

    # Clarification mode only for first vague query
    user_message_count = sum(1 for msg in messages if msg["role"] == "user")

    if is_vague(latest) and user_message_count == 1:
        return {
            "reply": "Can you tell me the role, seniority level, and required skills?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Recommendation + refinement mode
    recommendations = search_catalog(full_context, top_k=5)

    return {
        "reply": "Here are the updated SHL assessment recommendations based on your requirements.",
        "recommendations": [
            {
                "name": r["name"],
                "url": r["url"],
                "test_type": "Unknown"
            }
            for r in recommendations
        ],
        "end_of_conversation": False
    }