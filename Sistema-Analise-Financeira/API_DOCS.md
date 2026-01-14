# API Documentation - Sistema de Análise Financeira

## Endpoints

### GET /
**Descrição:** Página principal da aplicação
**Retorna:** HTML da interface do usuário

### POST /data
**Descrição:** Busca dados históricos e calcula indicadores técnicos

**Parâmetros:**
```json
{
  "symbol": "AAPL",        // Ticker da ação (obrigatório)
  "start": "2023-01-01",   // Data de início (YYYY-MM-DD)
  "end": "2023-12-31",     // Data de fim (YYYY-MM-DD)
  "horizon": 30            // Dias para previsão (opcional, padrão: 30)
}
```

**Resposta de Sucesso:**
```json
{
  "status": "ok",
  "meta": {
    "symbol": "AAPL",
    "name": "AAPL Stock",
    "horizon": 30
  },
  "candles": [
    {
      "Date": "2023-01-01",
      "Open": 150.0,
      "High": 155.0,
      "Low": 148.0,
      "Close": 152.0,
      "Volume": 1000000,
      "SMA_20": 151.5,
      "SMA_50": 150.8,
      "RSI": 65.2,
      "MACD": 1.2,
      "MACD_Signal": 0.8,
      "Upper_Band": 155.0,
      "Lower_Band": 148.0,
      "Pred": 151.8
    }
  ],
  "future": [
    {
      "Date": "2024-01-01",
      "Pred": 155.2
    }
  ]
}
```

### POST /download
**Descrição:** Gera e baixa arquivo Excel com dados e análises

**Parâmetros:** Mesmos do endpoint `/data`

**Resposta:** Arquivo Excel (.xlsx)

## Indicadores Técnicos Disponíveis

### Médias Móveis
- **SMA_20:** Média Móvel Simples de 20 períodos
- **SMA_50:** Média Móvel Simples de 50 períodos
- **EMA_12:** Média Móvel Exponencial de 12 períodos
- **EMA_26:** Média Móvel Exponencial de 26 períodos

### Osciladores
- **RSI:** Relative Strength Index (14 períodos)
- **MACD:** Moving Average Convergence Divergence
- **MACD_Signal:** Linha de sinal do MACD

### Bandas e Volatilidade
- **Upper_Band:** Banda Superior de Bollinger
- **Lower_Band:** Banda Inferior de Bollinger
- **ATR_14:** Average True Range de 14 períodos

### Volume
- **OBV:** On-Balance Volume

## Códigos de Erro

- **400:** Erro de validação nos parâmetros
- **404:** Ticker não encontrado
- **500:** Erro interno do servidor
- **503:** Serviço indisponível (problema com API externa)

## Exemplos de Uso

### JavaScript (Frontend)
```javascript
const response = await fetch('/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    symbol: 'AAPL',
    start: '2023-01-01',
    end: '2023-12-31',
    horizon: 30
  })
});

const data = await response.json();
```

### Python (Cliente)
```python
import requests

response = requests.post('http://localhost:5000/data', json={
    'symbol': 'AAPL',
    'start': '2023-01-01',
    'end': '2023-12-31',
    'horizon': 30
})

data = response.json()
```

## Configuração

### Variáveis de Ambiente
- `TWELVE_API_KEY`: Chave da API TwelveData (obrigatório)
- `FLASK_DEBUG`: Modo debug (True/False)
- `SECRET_KEY`: Chave secreta do Flask

### Arquivo .env
```
TWELVE_API_KEY=your_api_key_here
FLASK_DEBUG=False
SECRET_KEY=your_secret_key_here
```