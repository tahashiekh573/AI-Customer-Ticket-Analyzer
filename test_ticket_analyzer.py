
from src.data_loader import load_tickets, filter_tickets
from src.ticket_analyzer import analyze_ticket
from src.storage import save_results


def main():
    tickets = load_tickets()
    valid_tickets, filtered_tickets = filter_tickets(tickets)

    analyzed_tickets = []

    for _, ticket in valid_tickets.iterrows():
        analysis = analyze_ticket(ticket["message"])

        analyzed_tickets.append({
            "ticket_id": ticket["ticket_id"],
            "message": ticket["message"],
            **analysis,
        })

    print("\nCUSTOMER TICKET ANALYSIS")
    print("=" * 60)

    for ticket in analyzed_tickets:
        print(f"\nTicket ID: {ticket['ticket_id']}")
        print(f"Category: {ticket['category']}")
        print(f"Priority: {ticket['priority']}")
        print(f"Sentiment: {ticket['sentiment']}")
        print(f"Product/Feature: {ticket['product']}")
        print(f"Suggested Reply: {ticket['suggested_reply']}")

    analyzed_csv, filtered_csv, database_file = save_results(
        analyzed_tickets,
        filtered_tickets,
    )

    print("\n" + "=" * 60)
    print("PROCESSING SUMMARY")
    print("=" * 60)
    print(f"Total tickets: {len(tickets)}")
    print(f"Analyzed tickets: {len(analyzed_tickets)}")
    print(f"Ignored / rejected: {len(filtered_tickets)}")

    print("\nOUTPUT FILES")
    print("-" * 60)
    print(f"Analyzed CSV: {analyzed_csv}")
    print(f"Filtered CSV: {filtered_csv}")
    print(f"SQLite Database: {database_file}")


if __name__ == "__main__":
    main()