
from src.data_loader import load_tickets, filter_tickets


def main():
    tickets = load_tickets()
    valid_tickets, filtered_tickets = filter_tickets(tickets)

    print("\nCUSTOMER TICKET FILTERING REPORT")
    print("-" * 40)
    print(f"Total tickets: {len(tickets)}")
    print(f"Valid tickets: {len(valid_tickets)}")
    print(f"Ignored / rejected: {len(filtered_tickets)}")

    print("\nFILTERED MESSAGES")
    print("-" * 40)

    if filtered_tickets.empty:
        print("No messages were filtered.")
    else:
        print(
            filtered_tickets[
                ["ticket_id", "status", "reason"]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    main()