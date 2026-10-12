# InsightDesk — System Workflow

## 1. Project Overview

InsightDesk is a Python-based customer support ticket analysis system. It processes customer messages, filters invalid content, classifies support tickets, estimates sentiment and priority, detects potentially duplicate tickets, and stores results in structured formats.

## 2. System Workflow

### Step 1: Data Ingestion

The system reads customer support messages from `data/customer_tickets.csv`.

### Step 2: Data Validation and Filtering

The system validates incoming messages and filters out greeting-only messages, promotional spam, and other non-qualifying content.

### Step 3: Ticket Classification and Analysis

Each qualifying ticket is analyzed to identify:

* **Category:** Bug Report, Feature Request, Billing Issue, or General Inquiry.
* **Priority:** Low, Medium, High, or Urgent.
* **Sentiment:** Positive, Negative, or Neutral.
* **Product/Feature:** The recognized product or feature mentioned in the message.
* **Suggested Reply:** A short, polite response generated using predefined rules.

### Step 4: Duplicate Ticket Detection

The system uses TF-IDF vectorization and cosine similarity to identify potentially similar tickets. These results help support agents review recurring issues.

### Step 5: Data Storage and Export

The system stores or exports results to:

* `outputs/analyzed_tickets.csv` — analyzed tickets.
* `outputs/analyzed_tickets.json` — analyzed tickets in JSON format.
* `outputs/filtered_tickets.csv` — filtered or rejected messages.
* `outputs/tickets.db` — SQLite database.

### Step 6: Dashboard

The Streamlit dashboard allows users to explore ticket summaries, analyzed tickets, filtered messages, and potential duplicates.

## 3. How to Run

Open PowerShell in the project directory and activate the virtual environment:

```powershell
cd E:\AI-Customer-Ticket-Analyzer
.\venv\Scripts\Activate.ps1
```

Install dependencies if needed:

```powershell
python -m pip install -r requirements.txt
```

Run the dashboard:

```powershell
python -m streamlit run app.py --server.port 8502
```

Open `http://localhost:8502` in your browser.

## 4. Testing

Run the assessment and component tests:

```powershell
python test_data_loader.py
python test_ticket_analyzer.py
python test_duplicate_detector.py
python test_assessment_requirements.py
python -m pip check
```

## 5. Limitations

* Classification, priority, sentiment, and suggested replies use implemented rules rather than a trained AI model.
* Text similarity may identify tickets that are worded similarly but describe different issues.
* Support agents should review classifications and suggested replies before using them with customers.

## 6. Project Goal

InsightDesk demonstrates how Python, text processing, similarity detection, structured storage, and an interactive dashboard can help organize and review customer feedback more efficiently.
