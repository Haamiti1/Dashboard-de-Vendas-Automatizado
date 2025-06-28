from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from datetime import datetime, timedelta

app = Flask(__name__)

# Ajuste para seu banco remoto
engine = create_engine("sqlite:///vendas.db")  # ou PostgreSQL, MySQL...

@app.route('/api/dashboard')
def dashboard():
    periodo = request.args.get("periodo", "hoje")
    hoje = datetime.now()

    if periodo == "7dias":
        data_inicio = hoje - timedelta(days=7)
    elif periodo == "30dias":
        data_inicio = hoje - timedelta(days=30)
    elif periodo == "mes":
        data_inicio = hoje.replace(day=1)
    else:
        data_inicio = hoje.replace(hour=0, minute=0, second=0, microsecond=0)

    with engine.connect() as conn:
        result = conn.execute(f"""
            SELECT 
                SUM(valor_total) as total_vendas,
                COUNT(DISTINCT pedido_id) as total_pedidos,
                COUNT(DISTINCT cliente_id) as total_clientes
            FROM vendas
            WHERE data >= '{data_inicio.date()}'
        """).fetchone()

    return jsonify({
        "total_vendas": result.total_vendas or 0,
        "total_pedidos": result.total_pedidos or 0,
        "total_clientes": result.total_clientes or 0
    })

if __name__ == "__main__":
    app.run(debug=True)
