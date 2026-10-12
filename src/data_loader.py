
import re
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "customer_tickets.csv"

GREETING_MESSAGES = {
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
}

GREETING_ONLY_PATTERNS = [
    r"^(hi|hello|hey)\s+(hope you are having a nice day|hope you are doing well|how are you)$",
    r"^(good morning|good afternoon|good evening)(\s+how are you)?$",
]

PROMOTIONAL_KEYWORDS = {
    "buy followers",
    "you won a prize",
    "promotional offer",
    "click this promotional link",
    "limited time offer",
}


def load_tickets(file_path=DATA_FILE):
    """Load customer tickets from a CSV file."""

    if not Path(file_path).is_file():
        raise FileNotFoundError(
            f"Ticket dataset not found: {file_path}"
        )

    tickets = pd.read_csv(file_path)

    required_columns = {"ticket_id", "message"}
    missing_columns = required_columns.difference(tickets.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    tickets["ticket_id"] = (
        tickets["ticket_id"].fillna("").astype(str).str.strip()
    )
    tickets["message"] = (
        tickets["message"].fillna("").astype(str).str.strip()
    )

    return tickets


def classify_message(message):
    """Identify whether a message qualifies for ticket analysis."""

    if not isinstance(message, str):
        return "Rejected", "Invalid message format"

    normalized_message = re.sub(
        r"[^\w\s]", "", message.lower()
    ).strip()
    normalized_message = re.sub(
        r"\s+", " ", normalized_message
    )

    if not normalized_message:
        return "Rejected", "Empty message"

    if normalized_message in GREETING_MESSAGES:
        return "Ignored", "Greeting only"

    if any(
        re.fullmatch(pattern, normalized_message)
        for pattern in GREETING_ONLY_PATTERNS
    ):
        return "Ignored", "Greeting only"

    if any(
        keyword in normalized_message
        for keyword in PROMOTIONAL_KEYWORDS
    ):
        return "Rejected", "Promotional spam"

    if not re.search(r"[a-zA-Z]", normalized_message):
        return "Rejected", "No meaningful text"

    return "Valid", "Customer message"


def filter_tickets(tickets):
    """Separate valid customer messages from ignored or rejected messages."""

    results = tickets.copy()

    classifications = results["message"].apply(classify_message)

    results[["status", "reason"]] = pd.DataFrame(
        classifications.tolist(),
        index=results.index,
        columns=["status", "reason"],
    )

    valid_tickets = results[
        results["status"] == "Valid"
    ].copy()

    filtered_tickets = results[
        results["status"] != "Valid"
    ].copy()

    return valid_tickets, filtered_tickets