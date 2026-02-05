#!/usr/bin/env python3
"""
spendlocal - Your money. Your data. Your server.

A privacy-first expense tracker that runs on your own hardware.
https://github.com/rogi2709/spendlocal
"""

import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, g
from pathlib import Path

app = Flask(__name__)

# Configuration
DATABASE_PATH = Path.home() / "expenses.db"
HOST = "0.0.0.0"
PORT = 5000


def get_db():
    """Get database connection for current request."""
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    """Close database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def dashboard():
    """Render the expense dashboard."""
    db = get_db()

    # Get current month's data
    now = datetime.now()
    month_start = now.strftime("%Y-%m-01")
    month_name = now.strftime("%B %Y").upper()

    # Total spent this month
    total = db.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date >= ?",
        (month_start,)
    ).fetchone()["total"]

    # Card vs Cash breakdown
    card = db.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date >= ? AND account = 'Card'",
        (month_start,)
    ).fetchone()["total"]

    cash = db.execute(
        "SELECT COALESCE(SUM(amount), 0) as total FROM expenses WHERE date >= ? AND account = 'Cash'",
        (month_start,)
    ).fetchone()["total"]

    # Recent expenses
    recent = db.execute(
        "SELECT * FROM expenses ORDER BY date DESC, created_at DESC LIMIT 15"
    ).fetchall()

    return render_template(
        "index.html",
        month=month_name,
        total=total,
        card=card,
        cash=cash,
        expenses=recent,
        count=len(recent)
    )


@app.route("/add", methods=["POST"])
def add_expense():
    """Add a new expense via API."""
    data = request.get_json()

    # Validate required fields
    required = ["title", "amount", "account", "date"]
    missing = [f for f in required if f not in data or not data[f]]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Validate account type
    if data["account"] not in ["Card", "Cash"]:
        return jsonify({"error": "Account must be 'Card' or 'Cash'"}), 400

    # Validate amount
    try:
        amount = float(data["amount"])
        if amount <= 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"error": "Amount must be a positive number"}), 400

    # Insert into database
    db = get_db()
    db.execute(
        "INSERT INTO expenses (title, date, amount, account) VALUES (?, ?, ?, ?)",
        (data["title"], data["date"], amount, data["account"])
    )
    db.commit()

    return jsonify({"success": True, "message": "Expense added"})


@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=False)
