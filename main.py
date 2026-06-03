from fastapi import FastAPI
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

app = FastAPI()

def get_engine():
    return create_engine("postgresql+psycopg2://mdimranhosssan@localhost/expenses_db")

@app.get("/")
def home():
    return {"message": "💰 Expense Analyser API is running!"}

@app.get("/expenses")
def get_expenses():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM expenses ORDER BY date", engine)
    return df.to_dict(orient="records")

@app.get("/stats")
def get_stats():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM expenses", engine)
    amounts = np.array(df["amount"])
    return {
        "total": round(float(np.sum(amounts)), 2),
        "average": round(float(np.mean(amounts)), 2),
        "biggest": round(float(np.max(amounts)), 2),
        "smallest": round(float(np.min(amounts)), 2),
    }

@app.get("/expenses/by-category")
def by_category():
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM expenses", engine)
    result = df.groupby("category")["amount"].sum().sort_values(ascending=False)
    return result.to_dict()

@app.get("/expenses/{category}")
def by_specific_category(category: str):
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM expenses", engine)
    filtered = df[df["category"].str.lower() == category.lower()]
    return filtered.to_dict(orient="records")