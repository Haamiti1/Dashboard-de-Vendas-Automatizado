import subprocess
import threading
import time
import schedule
from enviar_email import gerar_relatorio
from atualizar_excel import atualizar

# ▶️ Rodar a API Flask em uma thread separada
def rodar_api():
    subprocess.run(["python", "app.py"])

# ▶️ Rodar atualização do Excel a cada 10 segundos
def agendar_atualizacao_excel():
    schedule.every(10).seconds.do(atualizar)
    while True:
        schedule.run_pending()
        time.sleep(1)

# ▶️ Agendar envio semanal de e-mail toda segunda às 08:00
def agendar_emails():
    schedule.every().monday.at("08:00").do(gerar_relatorio)
    while True:
        schedule.run_pending()
        time.sleep(60)

# ▶️ Disparar tudo
if __name__ == "__main__":
    print("🚀 Iniciando sistema completo...")

    threading.Thread(target=rodar_api, daemon=True).start()
    threading.Thread(target=agendar_atualizacao_excel, daemon=True).start()
    threading.Thread(target=agendar_emails, daemon=True).start()

    # Mantém o main vivo
    while True:
        time.sleep(10)
