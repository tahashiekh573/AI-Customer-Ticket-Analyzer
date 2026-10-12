
import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "outputs"
DATABASE_FILE = OUTPUT_DIR / "tickets.db"


def save_results(analyzed_tickets, filtered_tickets):
    """Save analyzed tickets to CSV and SQLite."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    analyzed_df = pd.DataFrame(analyzed_tickets)

    analyzed_csv = OUTPUT_DIR / "analyzed_tickets.csv"
    filtered_csv = OUTPUT_DIR / "filtered_tickets.csv"

    analyzed_df.to_csv(analyzed_csv, index=False)
    filtered_tickets.to_csv(filtered_csv, index=False)

    with sqlite3.connect(DATABASE_FILE) as connection:
        analyzed_df.to_sql(
            "analyzed_tickets",
            connection,
            if_exists="replace",
            index=False,
        )

        filtered_tickets.to_sql(
            "filtered_tickets",
            connection,
            if_exists="replace",
            index=False,
        )

    return analyzed_csv, filtered_csv, DATABASE_FILE