// Auto-fill end date
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('end').value = new Date().toISOString().slice(0,10);
});

async function buscarDados() {
    const ticker = document.getElementById('ticker').value.trim();
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value || new Date().toISOString().slice(0,10);
    const horizon = document.getElementById('horizon').value;
    
    const checkboxes = document.querySelectorAll('.indicator-checkbox input[type="checkbox"]:checked');
    const sel = Array.from(checkboxes).map(cb => cb.value);

    try {
        const res = await fetch('/data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol: ticker, start, end, horizon })
        });

        const payload = await res.json();
        if (!res.ok) {
            alert(payload.error || 'Erro ao buscar dados');
            return;
        }

        montarGraficos(payload, sel);
        
    } catch (err) {
        console.error(err);
        alert('Erro ao buscar dados: ' + err.message);
    }
}

function montarGraficos(payload, indicadores) {
    const data = payload.data;
    const future = payload.future;
    const meta = payload.meta;

    const dates = data.map(d => d.Date);
    const closes = data.map(d => d.Close);
    const volumes = data.map(d => d.Volume);

    // Layout base PREMIUM
    const baseLayout = {
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(255,255,255,0.02)',
        font: { color: '#ffffff', family: 'SF Pro Display, sans-serif', size: 12 },
        xaxis: { 
            gridcolor: 'rgba(255,255,255,0.08)',
            showgrid: true,
            zeroline: false,
            color: '#a1a1aa'
        },
        yaxis: { 
            gridcolor: 'rgba(255,255,255,0.08)',
            showgrid: true,
            zeroline: false,
            color: '#a1a1aa'
        },
        margin: { l: 60, r: 40, t: 60, b: 60 },
        hovermode: 'x unified',
        hoverlabel: {
            bgcolor: 'rgba(0,0,0,0.8)',
            bordercolor: '#6366f1',
            font: { color: '#ffffff' }
        }
    };

    // 1. PREÇO - Linha com gradiente
    Plotly.newPlot('precos', [{
        x: dates,
        y: closes,
        type: 'scatter',
        mode: 'lines',
        name: meta.symbol,
        line: { 
            color: '#6366f1', 
            width: 3,
            shape: 'spline'
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(99, 102, 241, 0.1)'
    }], {
        ...baseLayout,
        title: { 
            text: `💎 ${meta.symbol} - Preço`,
            font: { size: 20, color: '#ffffff' }
        },
        yaxis: { ...baseLayout.yaxis, title: 'Preço (USD)' },
        height: 450
    }, {responsive: true, displayModeBar: true});

    // 2. VOLUME - Barras coloridas
    const volumeColors = volumes.map((v, i) => {
        if (i === 0) return '#10b981';
        return closes[i] >= closes[i-1] ? '#10b981' : '#ef4444';
    });

    Plotly.newPlot('volume', [{
        x: dates,
        y: volumes,
        type: 'bar',
        name: 'Volume',
        marker: { 
            color: volumeColors,
            line: { width: 0 }
        }
    }], {
        ...baseLayout,
        title: { 
            text: '📊 Volume de Negociação',
            font: { size: 20, color: '#ffffff' }
        },
        yaxis: { ...baseLayout.yaxis, title: 'Volume' },
        height: 400
    }, {responsive: true, displayModeBar: true});

    // 3. RSI - Com zonas coloridas
    Plotly.newPlot('rsi', [{
        x: dates,
        y: data.map(d => d.RSI),
        type: 'scatter',
        mode: 'lines',
        name: 'RSI',
        line: { 
            color: '#8b5cf6', 
            width: 3
        },
        fill: 'tozeroy',
        fillcolor: 'rgba(139, 92, 246, 0.15)'
    }], {
        ...baseLayout,
        title: { 
            text: '⚡ RSI - Força Relativa',
            font: { size: 20, color: '#ffffff' }
        },
        yaxis: { ...baseLayout.yaxis, title: 'RSI', range: [0, 100] },
        shapes: [
            {
                type: 'rect',
                x0: dates[0],
                x1: dates[dates.length-1],
                y0: 70,
                y1: 100,
                fillcolor: 'rgba(239, 68, 68, 0.1)',
                line: { width: 0 }
            },
            {
                type: 'rect',
                x0: dates[0],
                x1: dates[dates.length-1],
                y0: 0,
                y1: 30,
                fillcolor: 'rgba(16, 185, 129, 0.1)',
                line: { width: 0 }
            },
            {
                type: 'line',
                x0: dates[0],
                x1: dates[dates.length-1],
                y0: 70,
                y1: 70,
                line: { color: '#ef4444', width: 2, dash: 'dash' }
            },
            {
                type: 'line',
                x0: dates[0],
                x1: dates[dates.length-1],
                y0: 30,
                y1: 30,
                line: { color: '#10b981', width: 2, dash: 'dash' }
            }
        ],
        height: 400
    }, {responsive: true, displayModeBar: true});

    // 4. MACD - Linhas + Histograma
    const macdHist = data.map(d => (d.MACD || 0) - (d.MACD_Signal || 0));
    const histColors = macdHist.map(v => v >= 0 ? '#10b981' : '#ef4444');

    Plotly.newPlot('macd', [
        {
            x: dates,
            y: macdHist,
            type: 'bar',
            name: 'Histograma',
            marker: { color: histColors }
        },
        {
            x: dates,
            y: data.map(d => d.MACD),
            type: 'scatter',
            mode: 'lines',
            name: 'MACD',
            line: { color: '#3b82f6', width: 2 }
        },
        {
            x: dates,
            y: data.map(d => d.MACD_Signal),
            type: 'scatter',
            mode: 'lines',
            name: 'Signal',
            line: { color: '#f59e0b', width: 2 }
        }
    ], {
        ...baseLayout,
        title: { 
            text: '📈 MACD - Momentum',
            font: { size: 20, color: '#ffffff' }
        },
        yaxis: { ...baseLayout.yaxis, title: 'MACD' },
        height: 400
    }, {responsive: true, displayModeBar: true});

    // 5. PREVISÃO - Multi-linha colorida
    const futureDates = future.map(f => f.Date);
    const futurePreds = future.map(f => f.Pred);

    Plotly.newPlot('previsao', [
        {
            x: dates,
            y: closes,
            type: 'scatter',
            mode: 'lines',
            name: 'Preço Real',
            line: { color: '#ffffff', width: 3 }
        },
        {
            x: dates,
            y: data.map(d => d.Pred),
            type: 'scatter',
            mode: 'lines',
            name: 'Ajuste ML',
            line: { color: '#10b981', width: 2, dash: 'dot' }
        },
        {
            x: futureDates,
            y: futurePreds,
            type: 'scatter',
            mode: 'lines+markers',
            name: 'Previsão Futura',
            line: { color: '#ef4444', width: 3 },
            marker: { size: 8, color: '#ef4444' }
        }
    ], {
        ...baseLayout,
        title: { 
            text: `🔮 Previsão ${meta.horizon} dias - Machine Learning`,
            font: { size: 20, color: '#ffffff' }
        },
        yaxis: { ...baseLayout.yaxis, title: 'Preço (USD)' },
        height: 450
    }, {responsive: true, displayModeBar: true});
}

async function baixarExcel() {
    const ticker = document.getElementById('ticker').value.trim();
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value || new Date().toISOString().slice(0,10);
    const horizon = document.getElementById('horizon').value;

    try {
        const res = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker, start, end, horizon })
        });

        if (!res.ok) {
            alert('Erro ao gerar Excel');
            return;
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${ticker}_analise_${new Date().toISOString().slice(0,10)}.xlsx`;
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        console.error(err);
        alert('Erro ao baixar arquivo');
    }
}

function toggleTheme() {
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
}


document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    }
});