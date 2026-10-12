# AI-Powered Customer Feedback & Support Ticket Analyzer

**InsightDesk** is a Python-based customer support ticket analysis system designed to organize customer feedback, classify support issues, estimate ticket priority and sentiment, and identify potentially duplicate tickets. It provides an interactive Streamlit dashboard to help support teams review and manage customer messages more efficiently.

## Features

* **Ticket Filtering:** Filters greeting-only messages and promotional spam.
* **Ticket Classification:** Categorizes tickets into bug reports, billing issues, feature requests, and general inquiries.
* **Priority Detection:** Assigns Low, Medium, High, or Urgent priority levels based on implemented rules.
* **Sentiment Analysis:** Classifies customer messages as Positive, Negative, or Neutral.
* **Product Identification:** Identifies the product or feature mentioned in a ticket.
* **Suggested Replies:** Generates rule-based response suggestions for support agents.
* **Duplicate Ticket Detection:** Uses TF-IDF vectorization and cosine similarity to identify potentially similar tickets.
* **Interactive Dashboard:** Provides views for ticket summaries, analyzed tickets, filtered messages, and potential duplicates.
* **Data Export and Storage:** Exports analysis results to CSV files and stores ticket data in an SQLite database.

## Technology Stack

* Python
* Streamlit
* Pandas
* Scikit-learn
* SQLite
* TF-IDF and cosine similarity

## Project Structure

```text
AI-Customer-Ticket-Analyzer/
├── data/
│   └── customer_tickets.csv
├── outputs/
│   ├── analyzed_tickets.csv
│   ├── filtered_tickets.csv
│   └── tickets.db
├── src/
├── app.py
├── requirements.txt
├── README.md
├── test_data_loader.py
├── test_ticket_analyzer.py
├── test_duplicate_detector.py
└── test_assessment_requirements.py
```

The `venv/` directory is created locally during setup and should not be included in the submission package.

## Installation and Setup

### 1. Open the project directory

Open PowerShell and navigate to the project folder:

```powershell
cd E:\AI-Customer-Ticket-Analyzer
```

### 2. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Run the dashboard

```powershell
python -m streamlit run app.py --server.port 8502
```

Open the following URL in your browser:

http://localhost:8502

If port 8502 is already in use, run the application with port 8503 instead.

## Running the Tests

Run each test script from the project directory:

```powershell
python test_data_loader.py
python test_ticket_analyzer.py
python test_duplicate_detector.py
python test_assessment_requirements.py
```

Verify dependency compatibility with:

```powershell
python -m pip check
```

## Output Files

| File                           | Description                                   |
| ------------------------------ | --------------------------------------------- |
| `data/customer_tickets.csv`    | Input dataset containing customer messages    |
| `outputs/analyzed_tickets.csv` | Structured analysis results for valid tickets |
| `outputs/filtered_tickets.csv` | Messages rejected during filtering            |
| `outputs/tickets.db`           | SQLite database for structured ticket data    |

## Validation and Test Results

During development, all four test scripts completed successfully. The tested scenarios included payment-page bug classification, dark-mode feature requests, greeting filtering, and duplicate-ticket detection. The dependency check also reported no broken requirements.

## Limitations

* Ticket classification, priority assignment, sentiment analysis, and suggested replies rely on implemented rules rather than a trained AI language model.
* Duplicate detection identifies text similarity, which does not always indicate identical underlying issues.
* Suggested replies and automated classifications should be reviewed by a support agent before operational use.

## Future Improvements

* Integrate a trained machine-learning model or large language model for improved ticket understanding.
* Improve sentiment analysis and priority prediction.
* Add ticket assignment, status tracking, and resolution workflows.
* Support additional input formats and larger datasets.
* Expand automated tests and introduce classification evaluation metrics.

## Project Objective

InsightDesk demonstrates how Python-based text processing, rule-based classification, similarity detection, structured data storage, and an interactive dashboard can support more efficient customer feedback analysis and ticket management.
