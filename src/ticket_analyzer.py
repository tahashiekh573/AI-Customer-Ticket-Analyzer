
import re


CATEGORY_KEYWORDS = {
    "Bug Report": [
        "crash", "crashes", "freezes", "bug", "error",
        "does nothing", "unable to access", "cannot log in",
        "cannot complete", "not working", "slower",
    ],
    "Feature Request": [
        "add", "introduce", "would be awesome",
        "could you add", "option to", "please add",
        "dark mode", "two-factor authentication",
        "download invoices as pdf",
    ],
    "Billing Issue": [
        "charged", "refund", "invoice shows",
        "billing cycle", "wrong amount", "charged twice",
        "payment issue", "billing issue",
    ],
}

URGENT_KEYWORDS = [
    "urgent", "asap", "immediately", "all users",
    "cannot complete my order", "every time",
]

HIGH_PRIORITY_KEYWORDS = [
    "crashes", "crash", "unable to access",
    "charged twice", "cannot log in", "wrong amount",
    "security issue",
]

NEGATIVE_KEYWORDS = [
    "crash", "crashes", "bug", "error", "cannot",
    "unable", "wrong", "refund", "freezes", "confusing",
    "difficult", "slower", "charged twice", "does nothing",
    "not working",
]

POSITIVE_KEYWORDS = [
    "love", "awesome", "perfectly", "thank you",
    "great", "excellent", "fast and easy",
]

PRODUCT_KEYWORDS = {
    "Payment Page": ["payment page", "checkout"],
    "Mobile App": ["mobile app", "mobile interface"],
    "Dashboard": ["dashboard"],
    "Subscription": ["subscription", "billing cycle"],
    "Login System": ["log in", "login", "password"],
    "Search Feature": ["search feature", "search"],
    "Invoice": ["invoice", "invoices"],
    "Excel Export": ["export to excel", "excel export"],
    "Dark Mode": ["dark mode"],
    "Security Settings": [
        "two-factor authentication",
        "account security",
    ],
    "Account Settings": ["account email"],
    "Application Access": [
        "access the application",
        "access the application",
    ],
}


def contains_keyword(text, keyword):
    """Check for a keyword without matching it inside other words."""

    pattern = rf"\b{re.escape(keyword)}\b"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def identify_category(message):
    """Classify a ticket using keywords and message intent."""

    text = message.lower()

    general_inquiry_phrases = [
        "how can i change my subscription plan",
        "how can i update my account",
        "please explain how",
    ]

    if any(phrase in text for phrase in general_inquiry_phrases):
        return "General Inquiry"

    billing_phrases = [
        "charged twice",
        "need a refund",
        "wrong amount",
        "invoice shows the wrong amount",
        "billing cycle",
        "payment issue",
    ]

    if any(phrase in text for phrase in billing_phrases):
        return "Billing Issue"

    scores = {
        category: sum(
            contains_keyword(text, keyword)
            for keyword in keywords
        )
        for category, keywords in CATEGORY_KEYWORDS.items()
    }

    if max(scores.values(), default=0) == 0:
        return "General Inquiry"

    highest_score = max(scores.values())
    matching_categories = [
        category
        for category, score in scores.items()
        if score == highest_score
    ]

    if len(matching_categories) > 1:
        if "Bug Report" in matching_categories:
            return "Bug Report"
        if "Billing Issue" in matching_categories:
            return "Billing Issue"

    return matching_categories[0]


def identify_priority(message):
    """Estimate priority using urgency and potential impact."""

    text = message.lower()
    category = identify_category(message)

    if any(contains_keyword(text, word) for word in URGENT_KEYWORDS):
        return "Urgent"

    if any(
        contains_keyword(text, word)
        for word in HIGH_PRIORITY_KEYWORDS
    ):
        return "High"

    if category in {
        "Bug Report",
        "Billing Issue",
        "Feature Request",
    }:
        return "Medium"

    return "Low"


def identify_sentiment(message):
    """Estimate sentiment from positive and negative expressions."""

    text = message.lower()

    negative_score = sum(
        contains_keyword(text, word)
        for word in NEGATIVE_KEYWORDS
    )
    positive_score = sum(
        contains_keyword(text, word)
        for word in POSITIVE_KEYWORDS
    )

    if negative_score > positive_score:
        return "Negative"

    if positive_score > negative_score:
        return "Positive"

    return "Neutral"


def identify_product(message):
    """Identify the most relevant product or feature mentioned."""

    text = message.lower()

    for product, keywords in PRODUCT_KEYWORDS.items():
        if any(
            contains_keyword(text, keyword)
            for keyword in keywords
        ):
            return product

    return "Not identified"


def generate_auto_reply(category, priority):
    """Create a polite draft response for the customer."""

    if priority == "Urgent":
        return (
            "Thank you for reporting this urgent issue. "
            "We understand its impact and will prioritize "
            "it for investigation."
        )

    replies = {
        "Bug Report": (
            "Thank you for reporting this issue. "
            "Our team will investigate it and work toward a fix."
        ),
        "Feature Request": (
            "Thank you for sharing your suggestion. "
            "We will review it for future improvements."
        ),
        "Billing Issue": (
            "Thank you for contacting us about billing. "
            "We will review the details and help resolve the issue."
        ),
        "General Inquiry": (
            "Thank you for contacting us. "
            "We will review your question and assist you."
        ),
    }

    return replies[category]


def analyze_ticket(message):
    """Extract structured information from a customer message."""

    if not isinstance(message, str) or not message.strip():
        raise ValueError("Ticket message must be a non-empty string.")

    category = identify_category(message)
    priority = identify_priority(message)

    return {
        "category": category,
        "priority": priority,
        "sentiment": identify_sentiment(message),
        "product": identify_product(message),
        "suggested_reply": generate_auto_reply(category, priority),
    }