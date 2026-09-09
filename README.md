# AI College Complaint Prioritizer

A complete college complaint management web application using Flask, SQLite and an explainable offline AI-style prioritization engine.

## Features

- Student complaint submission
- Automatic AI priority: Low / Medium / High / Critical
- Automatic urgency score from 0–100
- Explainable priority reason
- Complaint categories
- SQLite database
- Admin dashboard
- Sorts complaints by urgency
- Complaint status management
- JSON API for AI prioritization
- Responsive frontend
- No paid API key required

## Requirements

- Python 3.10+
- pip

## Run locally

### Windows

Open Command Prompt or PowerShell inside this folder:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

Dashboard:

http://127.0.0.1:5000/dashboard

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open:

http://127.0.0.1:5000

## Project structure

```text
ai_college_complaint_prioritizer/
├── app.py
├── ai_prioritizer.py
├── requirements.txt
├── README.md
├── complaints.db       # created automatically
├── templates/
│   ├── base.html
│   ├── index.html
│   └── dashboard.html
└── static/
    └── style.css
```

## API example

POST `/api/prioritize`

JSON:

```json
{
  "title": "Hostel water problem",
  "description": "There is no water in our hostel for two days.",
  "category": "Hostel"
}
```

Example response:

```json
{
  "priority": "High",
  "score": 48,
  "reason": "critical/urgent signals..."
}
```

## Important project note

The prioritizer is deliberately offline and explainable. It is suitable for a college prototype because it does not require an external AI service or API key. For a production deployment, replace or augment the rules with a trained NLP model and add authentication, authorization, audit logs, rate limiting, and stronger data protection.
