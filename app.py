from flask import Flask, jsonify, request, render_template_string
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

app = Flask(__name__)
engine = create_engine("sqlite:///vendas.db")

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>Dashboard de Vendas</title>
  <link rel="stylesheet" href="./css/style.css">
  <style>
    body { font-family: Arial, sans-serif; padding: 20px; background: #f9f9f9; }
    h1 { color: #333; }
    .card { background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 0 10px #ccc; }
    select { padding: 6px; font-size: 16px; margin-bottom: 20px; }
  </style>
</head>
<body>
  <h1>📊 Dashboard de Vendas</h1>
  <label for="periodo">Selecionar período:</label>
  <select id="periodo">
    <option value="hoje">Hoje</option>
    <option value="7dias">Últimos 7 dias</option>
    <option value="30dias">Últimos 30 dias</option>
    <option value="mes">Este mês</option>
  </select>

  <div class="card">
    <strong>Total de Vendas:</strong> R$ <span id="vendas">--</span>
  </div>
  <div class="card">
    <strong>Total de Pedidos:</strong> <span id="pedidos">--</span>
  </div>
  <div class="card">
    <strong>Total de Clientes:</strong> <span id="clientes">--</span>
  </div>

  <script>
    async function atualizarDashboard(periodo) {
      const res = await fetch('/api/dashboard?periodo=' + periodo);
      const data = await res.json();
      document.getElementById('vendas').textContent = data.total_vendas.toLocaleString('pt-BR', {minimumFractionDigits: 2});
      document.getElementById('pedidos').textContent = data.total_pedidos;
      document.getElementById('clientes').textContent = data.total_clientes;
    }

    document.getElementById('periodo').addEventListener('change', (e) => {
      atualizarDashboard(e.target.value);
    });

    atualizarDashboard('hoje'); // inicial
  </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML)

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
        query = text("""
            SELECT 
                SUM(valor_total) as total_vendas,
                COUNT(DISTINCT pedido_id) as total_pedidos,
                COUNT(DISTINCT cliente_id) as total_clientes
            FROM vendas
            WHERE data >= :data_inicio
        """)
        result = conn.execute(query, {"data_inicio": data_inicio}).fetchone()

    return jsonify({
        "total_vendas": float(result.total_vendas or 0),
        "total_pedidos": int(result.total_pedidos or 0),
        "total_clientes": int(result.total_clientes or 0)
    })

if __name__ == "__main__":
    app.run(debug=True)