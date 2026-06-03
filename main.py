import numpy as np
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

def connect():
    return psycopg2.connect(
        dbname="expenses_db",
        user="mdimranhosssan",
        host="localhost"
    )

def get_engine():
    return create_engine("postgresql+psycopg2://mdimranhosssan@localhost/expenses_db")

def setup_database():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id SERIAL PRIMARY KEY,
            date DATE,
            category VARCHAR(50),
            amount FLOAT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def import_csv_to_db():
    df = pd.read_csv("expenses.csv")
    conn = connect()
    cur = conn.cursor()
    
    # Clear existing data to avoid duplicates
    cur.execute("DELETE FROM expenses")
    
    for _, row in df.iterrows():
        cur.execute(
            "INSERT INTO expenses (date, category, amount) VALUES (%s, %s, %s)",
            (row["date"], row["category"], row["amount"])
        )
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Imported {len(df)} expenses to database!")

def analyse():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM expenses ORDER BY date", engine)
    
    df["date"] = pd.to_datetime(df["date"])
    amounts = np.array(df["amount"])

    print("=" * 40)
    print("💰 PERSONAL EXPENSE ANALYSER")
    print("   (data from PostgreSQL)")
    print("=" * 40)

    print(f"\n📊 Overall Stats:")
    print(f"  Total spent:     €{np.sum(amounts):.2f}")
    print(f"  Average/day:     €{np.mean(amounts):.2f}")
    print(f"  Biggest expense: €{np.max(amounts):.2f}")
    print(f"  Smallest:        €{np.min(amounts):.2f}")

    print(f"\n📂 Spending by Category:")
    by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    for category, total in by_category.items():
        print(f"  {category:<15} €{total:.2f}")

    print(f"\n🔝 Top 3 Biggest Expenses:")
    top3 = df.nlargest(3, "amount")[["date", "category", "amount"]]
    for _, row in top3.iterrows():
        print(f"  {row['date'].strftime('%Y-%m-%d')}  {row['category']:<15} €{row['amount']:.2f}")

    print(f"\n📅 Daily Spending:")
    by_date = df.groupby("date")["amount"].sum()
    for date, total in by_date.items():
        bar = "█" * int(total / 10)
        print(f"  {date.strftime('%b %d')}  {bar} €{total:.2f}")

def main():
    setup_database()
    import_csv_to_db()
    analyse()

if __name__ == "__main__":
    main()