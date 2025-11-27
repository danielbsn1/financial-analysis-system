async function buscarDados() {
    const ticker = document.getElementById('ticker').value.trim();
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value || new Date().toISOString().slice(0,10);
    const horizon = document.getElementById('horizon').value;
    const sel = Array.from(document.getElementById('indicator_select').selectedOptions).map(o => o.value);

    if (!ticker) { alert('Informe um ticker'); return; }

    const body = { ticker, start, end, horizon };

    try {
        const res = await fetch('/get_data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        const payload = await res.json();
        if (!res.ok) {
            alert(payload.error || 'Erro ao buscar dados');
            return;
        }

        montarGraficos(payload, sel);
    } catch (err) {
        console.error(err);
        alert('Erro na comunicação com o servidor');
    }
}

function montarGraficos(payload, indicadores) {
    const data = payload.data;
    const future = payload.future;

    const dates = data.map(d => d.Date);
    const opens = data.map(d => d.Open);
    const highs = data.map(d => d.High);
    const lows = data.map(d => d.Low);
    const closes = data.map(d => d.Close);
    const volumes = data.map(d => d.Volume);

    // Candlestick principal
    const candleTrace = {
        x: dates,
        open: opens,
        high: highs,
        low: lows,
        close: closes,
        type: 'candlestick',
        name: payload.meta.ticker
    };

    const addTraces = [candleTrace];

    if (indicadores.includes('sma')) {
        addTraces.push({ x: dates, y: data.map(d => d.SMA_20), name: 'SMA20', type: 'scatter' });
        addTraces.push({ x: dates, y: data.map(d => d.SMA_50), name: 'SMA50', type: 'scatter' });
    }

    if (indicadores.includes('ema')) {
        addTraces.push({ x: dates, y: data.map(d => d.EMA_12), name: 'EMA12', type: 'scatter' });
        addTraces.push({ x: dates, y: data.map(d => d.EMA_26), name: 'EMA26', type: 'scatter' });
    }

    if (indicadores.includes('boll')) {
        addTraces.push({ x: dates, y: data.map(d => d.Upper_Band), name: 'Upper Band', line: { dash: 'dot' }, type: 'scatter' });
        addTraces.push({ x: dates, y: data.map(d => d.Lower_Band), name: 'Lower Band', line: { dash: 'dot' }, type: 'scatter' });
    }

    // Add in-sample prediction
    addTraces.push({ x: dates, y: data.map(d => d.Pred), name: 'Predição (in-sample)', line: { dash: 'dash' }, type: 'scatter' });

    Plotly.newPlot('precos', addTraces, { title: `${payload.meta.ticker} - Preço` });

    // Volume
    Plotly.newPlot('volume', [
        { x: dates, y: volumes, type: 'bar', name: 'Volume' }
    ], { title: 'Volume' });

    // RSI
    if (indicadores.includes('rsi')) {
        Plotly.newPlot('rsi', [
            { x: dates, y: data.map(d => d.RSI), type: 'scatter', name: 'RSI' }
        ], { title: 'RSI' });
    } else {
        Plotly.newPlot('rsi', [
            { x: dates, y: data.map(d => d.RSI), type: 'scatter', name: 'RSI' }
        ], { title: 'RSI (toggle para esconder)' });
    }

    // MACD
    Plotly.newPlot('macd', [
        { x: dates, y: data.map(d => d.MACD), name: 'MACD', type: 'scatter' },
        { x: dates, y: data.map(d => d.MACD_Signal), name: 'Signal', type: 'scatter' }
    ], { title: 'MACD' });

    // Previsão futura (concatena histórico + futuro)
    const futureDates = future.map(f => f.Date);
    const futurePreds = future.map(f => f.Pred);

    Plotly.newPlot('previsao', [
        { x: dates, y: closes, name: 'Real', type: 'scatter' },
        { x: dates.concat(futureDates), y: data.map(d => d.Pred).concat(futurePreds), name: 'Previsão (in-sample + future)', type: 'scatter' },
        { x: futureDates, y: futurePreds, name: 'Previsão futura', mode: 'lines+markers', line: { dash: 'dot' } }
    ], { title: `Previsão para ${payload.meta.horizon} dias` });
}

async function baixarExcel() {
    const ticker = document.getElementById('ticker').value.trim();
    const start = document.getElementById('start').value;
    const end = document.getElementById('end').value || new Date().toISOString().slice(0,10);
    const horizon = document.getElementById('horizon').value;

    const body = { ticker, start, end, horizon };

    try {
        const res = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!res.ok) {
            const err = await res.json();
            alert(err.error || 'Erro ao gerar Excel');
            return;
        }

        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${ticker}_data_${start}_to_${end}.xlsx`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
    } catch (err) {
        console.error(err);
        alert('Erro ao baixar o arquivo');
    }
}

function toggleTheme() {
    const page = document.getElementById('page');
    page.classList.toggle('dark');
}

// Auto-fill end date with today if e
document.getElementById('end').value = new Date().toISOString().slice(0,10);