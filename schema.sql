-- Simple Expense Tracker - Database Schema

CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    account TEXT NOT NULL CHECK (account IN ('Card', 'Cash')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for faster monthly queries
CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(date);
