import numpy as np
import pandas as pd

# Read from CSV file instead of hardcoded data
df = pd.read_csv("expenses.csv")
df["date"] = pd.to_datetime(df["date"])

print("=" * 40)
print("💰 PERSONAL EXPENSE ANALYSER")
print(f"   Loaded {len(df)} expenses from expenses.csv")
print("=" * 40)

# --- NUMPY: basic stats ---
amounts = np.array(df["amount"])
print(f"\n📊 Overall Stats:")
print(f"  Total spent:     €{np.sum(amounts):.2f}")
print(f"  Average/day:     €{np.mean(amounts):.2f}")
print(f"  Biggest expense: €{np.max(amounts):.2f}")
print(f"  Smallest:        €{np.min(amounts):.2f}")

# --- PANDAS: by category ---
print(f"\n📂 Spending by Category:")
by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
for category, total in by_category.items():
    print(f"  {category:<15} €{total:.2f}")

# --- PANDAS: top 3 ---
print(f"\n🔝 Top 3 Biggest Expenses:")
top3 = df.nlargest(3, "amount")[["date", "category", "amount"]]
for _, row in top3.iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}  {row['category']:<15} €{row['amount']:.2f}")

# --- PANDAS: daily trend ---
print(f"\n📅 Daily Spending:")
by_date = df.groupby("date")["amount"].sum()
for date, total in by_date.items():
    bar = "█" * int(total / 10)
    print(f"  {date.strftime('%b %d')}  {bar} €{total:.2f}")

print("\n✅ Data loaded from expenses.csv")