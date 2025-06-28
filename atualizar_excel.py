import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///vendas.db")

def atualizar():
    df = pd.read_excel("vendas.xlsx")
    df.columns = df.columns.str.strip().str.lower()
    df["data"] = pd.to_datetime(df["data"])
    df.to_sql("vendas", engine, if_exists="replace", index=False)
    print("📥 Base atualizada.")