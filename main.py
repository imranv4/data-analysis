import numpy as np
import pandas as pd

# Sample expense data
data = {
    "date": [
        "2026-05-01", "2026-05-02", "2026-05-03", "2026-05-04", "2026-05-05",
        "2026-05-06", "2026-05-07", "2026-05-08", "2026-05-09", "2026-05-10",
        "2026-05-11", "2026-05-12", "2026-05-13", "2026-05-14", "2026-05-15"
    ],
    "category": [
        "Food", "Transport", "Food", "Entertainment", "Food",
        "Rent", "Food", "Transport", "Shopping", "Food",
        "Entertainment", "Food", "Transport", "Shopping", "Food"
    ],
    "amount": [
        12.50, 3.20, 8.75, 25.00, 15.30,
        800.00, 9.40, 4.50, 45.00, 11.20,
        30.00, 7.80, 3.90, 60.00, 13.50
    ]
}

# Create a pandas DataFrame (like a table)
df = pd.DataFrame(data)
df["date"] = pd.to_datetime(df["date"])

print("=" * 40)
print("💰 PERSONAL EXPENSE ANALYSER")
print("=" * 40)

# --- NUMPY: basic stats on amounts ---
amounts = np.array(df["amount"])
print(f"\n📊 Overall Stats:")
print(f"  Total spent:    €{np.sum(amounts):.2f}")
print(f"  Average/day:    €{np.mean(amounts):.2f}")
print(f"  Biggest expense:€{np.max(amounts):.2f}")
print(f"  Smallest:       €{np.min(amounts):.2f}")

# --- PANDAS: spending by category ---
print(f"\n📂 Spending by Category:")
by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
for category, total in by_category.items():
    print(f"  {category:<15} €{total:.2f}")

# --- PANDAS: top 3 biggest expenses ---
print(f"\n🔝 Top 3 Biggest Expenses:")
top3 = df.nlargest(3, "amount")[["date", "category", "amount"]]
for _, row in top3.iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}  {row['category']:<15} €{row['amount']:.2f}")

# --- PANDAS: daily spending trend ---
print(f"\n📅 Daily Spending:")
by_date = df.groupby("date")["amount"].sum()
for date, total in by_date.items():
    bar = "█" * int(total / 10)
    print(f"  {date.strftime('%b %d')}  {bar} €{total:.2f}")