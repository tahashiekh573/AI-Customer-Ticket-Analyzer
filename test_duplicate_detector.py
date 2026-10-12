
import pandas as pd

from src.duplicate_detector import find_similar_tickets


def test_similar_tickets():
    tickets = pd.DataFrame([
        {
            "ticket_id": "TKT-101",
            "message": "The payment page crashes during checkout",
        },
        {
            "ticket_id": "TKT-102",
            "message": "Payment page crashes when I try checkout",
        },
        {
            "ticket_id": "TKT-103",
            "message": "Please add a dark mode to the mobile app",
        },
    ])

    matches = find_similar_tickets(tickets, threshold=0.30)

    assert not matches.empty, "Expected similar tickets to be detected"

    pair = matches[
        (matches["ticket_id_1"] == "TKT-101")
        & (matches["ticket_id_2"] == "TKT-102")
    ]

    assert not pair.empty, "Expected payment tickets to match"

    print("PASS: Similar payment tickets detected")
    print(matches.to_string(index=False))


if __name__ == "__main__":
    test_similar_tickets()