const ctx = document.getElementById("dashboardChart").getContext("2d");
let chart;

function carregarDados(periodo) {
    fetch(`http://localhost:5000/api/dashboard?periodo=${periodo}`)
    .then(res => res.json())
    .then(data => {
    const dados = {
        labels: ["Total de Vendas", "Total de Pedidos", "Total de Clientes"],
        datasets: [{
        label: "Resumo",
        data: [data.total_vendas, data.total_pedidos, data.total_clientes],
        backgroundColor: ["#4caf50", "#2196f3", "#ffc107"]
        }]
     };

    if (chart) {
        chart.data = dados;
        chart.update();
    }
    else {
        chart = new Chart(ctx, {
            type: "bar",
            data: dados,
            options: {
                plugins: {
                    legend: { display: false },
                    title: { display: true, text: "Resumo de Vendas" }
                }
            }
        });
}});
}

document.getElementById("filtroPeriodo").addEventListener("change", e => {
    carregarDados(e.target.value);
});

carregarDados("hoje");