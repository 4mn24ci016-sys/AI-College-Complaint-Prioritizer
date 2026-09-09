"""
AI College Complaint Prioritizer - One-Click Launcher.
Trains ML model if missing and starts the FastAPI server.
"""

import sys
import uvicorn
from ml.train import load_trained_models


def main():
    print("=" * 70)
    print("  AI College Complaint Prioritizer & Redressal System")
    print("=" * 70)
    print(">>> Initializing AI classification models...")
    load_trained_models()
    print(">>> AI Engine ready.")
    print(">>> Starting Web Server on http://127.0.0.1:8000")
    print(">>> Student Portal:      http://127.0.0.1:8000")
    print(">>> Admin Triage Board:  http://127.0.0.1:8000/admin")
    print(">>> OpenAPI Docs:        http://127.0.0.1:8000/docs")
    print("=" * 70)

    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    main()
