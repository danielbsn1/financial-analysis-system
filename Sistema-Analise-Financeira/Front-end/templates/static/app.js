document.addEventListener('DOMContentLoaded', () => {
        const loadDataBtn = document.getElementById('loadDataBtn');
        const tickerInput = document.getElementById('ticker');
        const statsDiv = document.getElementById('stats');
        const errorDiv = document.getElementById('error');
        const priceChartDiv = document.getElementById('priceChart');
        const returnChartDiv = document.getElementById('returnChart');

        loadDataBtn.addEventListener('click', () => {
            const ticker = tickerInput.value.trim().toUpperCase();
            if (!ticker) {
                errorDiv.textContent = 'Por favor, insira um ticker válido.';
                statsDiv.innerHTML = '';
                priceChartDiv.innerHTML = '';
                returnChartDiv.innerHTML = '';
                return;
            }
            errorDiv.textContent = '';
            statsDiv.innerHTML = 'Carregando dados...';
            priceChartDiv.innerHTML = '';
            returnChartDiv.innerHTML = '';

            fetch('/get_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ticker })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    errorDiv.textContent = data.error;
                    statsDiv.innerHTML = '';
                    return;
                }
                errorDiv.textContent = '';
                mostrarEstatisticas(data.stats);
                mostrarGraficos(data);
            })
            .catch(err => {
                errorDiv.textContent = 'Erro ao carregar os dados.';
                statsDiv.innerHTML = '';
                console.error(err);
            });
        });

        function mostrarEstatisticas(stats) {
            statsDiv.innerHTML = `
                <h3>Estatísticas</h3>
                <ul>
                    <li><b>Volatilidade anualizada:</b> ${ (stats.volatility * 100).toFixed(2) } %</li>
                    <li><b>Retorno anualizado médio:</b> ${ (stats.annual_return * 100).toFixed(2) } %</li>
                    <li><b>Correlação entre variáveis:</b> <pre>${JSON.stringify(stats.correlation, null, 2)}</pre></li>
                </ul>
            `;
        }

        function mostrarGraficos(data) {
            const traceClose = {
                x: data.dates,
                y: data.close,
                type: 'scatter',
                mode: 'lines',
                name: 'Preço Fechamento'
            };
            const traceMA20 = {
                x: data.dates,
                y: data.ma20,
                type: 'scatter',
                mode: 'lines',
                name: 'Média Móvel 20'
            };
            const layoutPrice = {
                title: 'Preço Fechamento e Média Móvel 20',
                xaxis: { title: 'Data' },
                yaxis: { title: 'Preço' }
            };

            Plotly.newPlot(priceChartDiv, [traceClose, traceMA20], layoutPrice);

            const traceReturn = {
                x: data.dates,
                y: data.return.map(r => r * 100),
                type: 'bar',
                name: 'Retorno Diário (%)'
            };
            const layoutReturn = {
                title: 'Retorno Diário em %',
                xaxis: { title: 'Data' },
                yaxis: { title: 'Retorno (%)' }
            };

            Plotly.newPlot(returnChartDiv, [traceReturn], layoutReturn);
        }
    });