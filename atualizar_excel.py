import pandas as pd
from sqlalchemy import create_engine
import schedule
import time

engine = create_engine("sqlite:///vendas.db")  # ou PostgreSQL

def atualizar():
    df = pd.read_excel("vendas.xlsx")
    df["data"] = pd.to_datetime(df["data"])
    
    with engine.begin() as conn:
        conn.execute("DROP TABLE IF EXISTS vendas")
        df.to_sql("vendas", con=conn, index=False)

schedule.every(10).seconds.do(atualizar)

print("Agendador rodando...")

while True:
    schedule.run_pending()
    time.sleep(1)
