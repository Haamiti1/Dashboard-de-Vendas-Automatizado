import pandas as pd
import yagmail
from datetime import datetime, timedelta
from sqlalchemy import create_engine

EMAIL = "teuemail@gmail.com"
SENHA = "tua-senha-de-app"
DESTINATARIOS = ["destino@exemplo.com"]

engine = create_engine("sqlite:///vendas.db")

def gerar_relatorio():
    hoje = datetime.now()
    inicio_semana = hoje - timedelta(days=7)

    query = f"SELECT * FROM vendas WHERE data >= '{inicio_semana.strftime('%Y-%m-%d')}'"
    df = pd.read_sql_query(query, engine)

    nome_arquivo = f"relatorio_{hoje.strftime('%Y%m%d')}.xlsx"
    df.to_excel(nome_arquivo, index=False)

    yag = yagmail.SMTP(EMAIL, SENHA)
    yag.send(
        to=DESTINATARIOS,
        subject="📊 Relatório Semanal de Vendas",
        contents=f"Segue anexo o relatório da semana de {inicio_semana.date()} a {hoje.date()}",
        attachments=nome_arquivo
    )

    print("📧 E-mail enviado!")
