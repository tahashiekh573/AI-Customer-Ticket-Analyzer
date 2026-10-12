
from src.ticket_analyzer import analyze_ticket
from src.data_loader import classify_message


def test_payment_page_bug():
    message = (
        "The payment page crashes every time I click "
        "'Checkout' on Chrome. Please fix this ASAP!"
    )

    result = analyze_ticket(message)

    assert result["category"] == "Bug Report"
    assert result["priority"] == "Urgent"
    assert result["sentiment"] == "Negative"

    print("PASS: Payment page bug scenario")


def test_dark_mode_feature_request():
    message = (
        "Hi team, it would be awesome if you could "
        "add a dark mode to the mobile app."
    )

    result = analyze_ticket(message)

    assert result["category"] == "Feature Request"
    assert result["priority"] == "Medium"
    assert result["sentiment"] == "Positive"

    print("PASS: Dark mode feature request scenario")


def test_greeting_is_ignored():
    message = "Hello, hope you are having a nice day!"

    status, reason = classify_message(message)

    assert status == "Ignored"
    assert reason == "Greeting only"

    print("PASS: Greeting filtering scenario")


if __name__ == "__main__":
    test_payment_page_bug()
    test_dark_mode_feature_request()
    test_greeting_is_ignored()

    print("\nAll assessment scenario tests passed!")