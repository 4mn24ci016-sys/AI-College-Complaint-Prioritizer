from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
from datetime import datetime
from ai_prioritizer import prioritize_complaint

app = Flask(__name__)
app.secret_key = "college-complaint-demo-key"
DB = "complaints.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL,
            score INTEGER NOT NULL,
            reason TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    conn = get_db()
    complaints = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC LIMIT 8"
    ).fetchall()
    conn.close()
    return render_template("index.html", complaints=complaints)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("student_name", "").strip()
    email = request.form.get("student_email", "").strip()
    category = request.form.get("category", "Other")
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not all([name, email, title, description]):
        flash("Please complete all required fields.", "error")
        return redirect(url_for("index"))

    result = prioritize_complaint(title, description, category)

    conn = get_db()
    conn.execute("""
        INSERT INTO complaints
        (student_name, student_email, category, title, description,
         priority, score, reason, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending', ?)
    """, (
        name, email, category, title, description,
        result["priority"], result["score"], result["reason"],
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

    flash(
        f"Complaint submitted successfully. AI priority: {result['priority']}.",
        "success"
    )
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    conn = get_db()
    complaints = conn.execute(
        "SELECT * FROM complaints ORDER BY score DESC, id DESC"
    ).fetchall()

    stats = {
        "total": conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0],
        "critical": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE priority='Critical'"
        ).fetchone()[0],
        "high": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE priority='High'"
        ).fetchone()[0],
        "medium": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE priority='Medium'"
        ).fetchone()[0],
        "low": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE priority='Low'"
        ).fetchone()[0],
        "pending": conn.execute(
            "SELECT COUNT(*) FROM complaints WHERE status='Pending'"
        ).fetchone()[0],
    }
    conn.close()
    return render_template("dashboard.html", complaints=complaints, stats=stats)

@app.route("/update-status/<int:complaint_id>", methods=["POST"])
def update_status(complaint_id):
    status = request.form.get("status", "Pending")
    allowed = {"Pending", "In Progress", "Resolved", "Rejected"}
    if status not in allowed:
        return jsonify({"error": "Invalid status"}), 400

    conn = get_db()
    conn.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        (status, complaint_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for("dashboard"))

@app.route("/api/prioritize", methods=["POST"])
def api_prioritize():
    data = request.get_json(silent=True) or {}
    result = prioritize_complaint(
        data.get("title", ""),
        data.get("description", ""),
        data.get("category", "Other")
    )
    return jsonify(result)

init_db()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
