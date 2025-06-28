import pandas as pd
from sqlalchemy import create_engine
import schedule
import time
import os

# Criando conexão com o banco (pode ser SQLite, PostgreSQL etc.)
engine = create_engine("sqlite:///vendas.db")

def atualizar():
    try:
        # Verifica se o arquivo existe
        if not os.path.exists("vendas.xlsx"):
            print("❌ Arquivo 'vendas.xlsx' não encontrado.")
            return
        
        df = pd.read_excel("vendas.xlsx")

        # Limpa e normaliza os nomes das colunas
        df.columns = df.columns.str.strip().str.lower()
        print("✅ Colunas encontradas:", df.columns.tolist())

        # Verifica se a coluna 'data' existe
        if 'data' not in df.columns:
            print("❌ A coluna 'data' não foi encontrada no Excel.")
            return

        # Converte a coluna 'data' para datetime
        df["data"] = pd.to_datetime(df["data"])

        # Escreve no banco de dados
        df.to_sql("vendas", con=engine, if_exists="replace", index=False)
        print("✅ Dados atualizados no banco com sucesso.")

    except Exception as e:
        print("❌ Erro durante atualização:", e)

# Agenda para rodar a cada 10 segundos
schedule.every(10).seconds.do(atualizar)

print("🕒 Agendador rodando... Pressione CTRL+C para parar.")

# Loop principal
while True:
    schedule.run_pending()
    time.sleep(1)
