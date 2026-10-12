
from difflib import SequenceMatcher

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_similar_tickets(
    tickets: pd.DataFrame,
    threshold: float = 0.35,
) -> pd.DataFrame:
    """Find pairs of customer tickets with similar messages."""

    required_columns = {"ticket_id", "message"}
    missing = required_columns.difference(tickets.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    columns = [
        "ticket_id_1",
        "ticket_id_2",
        "similarity",
        "message_1",
        "message_2",
    ]

    data = tickets[["ticket_id", "message"]].copy()
    data["message"] = data["message"].fillna("").astype(str).str.strip()
    data = data[data["message"] != ""].reset_index(drop=True)

    if len(data) < 2:
        return pd.DataFrame(columns=columns)

    if not 0 <= threshold <= 1:
        raise ValueError("threshold must be between 0 and 1")

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english",
        ngram_range=(1, 2),
    )

    try:
        matrix = vectorizer.fit_transform(data["message"])
    except ValueError:
        # For example, messages containing only stop words.
        return pd.DataFrame(columns=columns)

    similarities = cosine_similarity(matrix)
    matches = []

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            score = float(similarities[i, j])

            if score >= threshold:
                matches.append({
                    "ticket_id_1": data.iloc[i]["ticket_id"],
                    "ticket_id_2": data.iloc[j]["ticket_id"],
                    "similarity": round(score, 3),
                    "message_1": data.iloc[i]["message"],
                    "message_2": data.iloc[j]["message"],
                })

    result = pd.DataFrame(matches, columns=columns)

    if not result.empty:
        result = result.sort_values(
            "similarity",
            ascending=False,
        ).reset_index(drop=True)

    return result