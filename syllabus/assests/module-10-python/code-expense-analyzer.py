"""
Expense Analyzer — Module 10 Code Snap
Run: python code-expense-analyzer.py
Creates sample CSV if not found, then analyzes it.
"""
import csv
import os
from collections import defaultdict

CSV_FILE = "expenses.csv"

SAMPLE_DATA = [
    ("2026-01-05", "Chai and samosa", "Food", 50),
    ("2026-01-05", "Bus ticket", "Transport", 30),
    ("2026-01-06", "Notebook and pen", "Study", 120),
    ("2026-01-06", "Lunch thali", "Food", 80),
    ("2026-01-07", "Mobile recharge", "Phone", 299),
    ("2026-01-08", "Auto to college", "Transport", 60),
    ("2026-01-08", "Movie ticket", "Entertainment", 250),
    ("2026-01-09", "Python book", "Study", 450),
    ("2026-01-10", "Dinner with friends", "Food", 350),
    ("2026-01-10", "Uber ride", "Transport", 180),
    ("2026-01-12", "Coffee", "Food", 40),
    ("2026-01-13", "Gym monthly", "Health", 800),
    ("2026-01-14", "Grocery", "Food", 500),
    ("2026-01-15", "Internet bill", "Phone", 599),
    ("2026-01-16", "Popcorn at mall", "Entertainment", 200),
    ("2026-01-18", "Bus pass monthly", "Transport", 400),
    ("2026-01-20", "Haircut", "Personal", 200),
    ("2026-01-22", "Domain name", "Study", 799),
    ("2026-01-25", "Birthday gift", "Personal", 600),
    ("2026-01-28", "Medicine", "Health", 350),
]


def create_sample_csv():
    """Create sample expense CSV if it doesn't exist."""
    if os.path.exists(CSV_FILE):
        return

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "description", "category", "amount"])
        writer.writerows(SAMPLE_DATA)
    print(f"Created sample file: {CSV_FILE}")


def read_expenses():
    """Read expenses from CSV file."""
    expenses = []
    try:
        with open(CSV_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["amount"] = float(row["amount"])
                expenses.append(row)
    except FileNotFoundError:
        print(f"Error: {CSV_FILE} not found!")
    return expenses


def category_totals(expenses):
    """Calculate total spending per category."""
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return dict(sorted(totals.items(), key=lambda x: x[1], reverse=True))


def highest_expense(expenses):
    """Find the single highest expense."""
    return max(expenses, key=lambda e: e["amount"])


def daily_average(expenses):
    """Calculate average daily spending."""
    unique_days = len(set(e["date"] for e in expenses))
    total = sum(e["amount"] for e in expenses)
    return total / unique_days if unique_days else 0


def print_report(expenses):
    """Print formatted expense report."""
    total = sum(e["amount"] for e in expenses)

    print("\n" + "=" * 50)
    print("      EXPENSE ANALYSIS REPORT")
    print("=" * 50)

    print(f"\nTotal Transactions: {len(expenses)}")
    print(f"Total Spending:     ₹{total:,.0f}")
    print(f"Daily Average:      ₹{daily_average(expenses):,.0f}")

    print(f"\n{'Category':<18} {'Amount':>10} {'  %':>6}")
    print("-" * 36)
    for cat, amount in category_totals(expenses).items():
        pct = (amount / total) * 100
        bar = "#" * int(pct / 3)
        print(f"{cat:<18} ₹{amount:>8,.0f}  {pct:>5.1f}%  {bar}")

    top = highest_expense(expenses)
    print(f"\nHighest Expense:")
    print(f"  {top['description']} — ₹{top['amount']:,.0f} ({top['date']})")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    create_sample_csv()
    expenses = read_expenses()
    if expenses:
        print_report(expenses)
