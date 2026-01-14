# 📚 Documentação da API

## Base URL
```
http://localhost:5001
```

## Endpoints

### 1. Página Principal
```http
GET /
```

**Resposta:** HTML da interface do usuário

---

### 2. Buscar Dados de Ações
```http
POST /data
```

**Request Body:**
```json
{
  "symbol": "AAPL",
  "start": "2024-01-01",
  "end": "2024-12-31",
  "horizon": 30
}
```

**Parâmetros:**
| Campo | Tipo | Obrigatório | Descrição |
|-------|------|-------------|-----------|
| symbol | string | Sim | Ticker da ação (ex: AAPL, TSLA) |
| start | string | Sim | Data início (YYYY-MM-DD) |
| end | string | Sim | Data fim (YYYY-MM-DD) |
| horizon | integer | Não | Dias para previsão (padrão: 30) |

**Resposta de Sucesso (200):**
```json
{
  "status": "ok",
  "meta": {
    "symbol": "AAPL",
    "name": "AAPL Stock",
    "horizon": 30
  },
  "data": [
    {
      "Date": "2024-01-01",
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
      "Date": "2024-02-01",
      "Pred": 155.2
    }
  ]
}
```

**Resposta de Erro (400):**
```json
{
  "error": "Erro: Ticker não encontrado"
}
```

---

### 3. Download Excel
```http
POST /download
```

**Request Body:**
```json
{
  "ticker": "AAPL",
  "start": "2024-01-01",
  "end": "2024-12-31",
  "horizon": 30
}
```

**Resposta:** Arquivo Excel (.xlsx)

**Headers:**
```
Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
Content-Disposition: attachment; filename="AAPL_analise_20241231.xlsx"
```

---

## Códigos de Status

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Erro de validação |
| 404 | Recurso não encontrado |
| 500 | Erro interno do servidor |

## Exemplos de Uso

### cURL
```bash
curl -X POST http://localhost:5001/data \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "start": "2024-01-01",
    "end": "2024-12-31",
    "horizon": 30
  }'
```

### Python
```python
import requests

response = requests.post('http://localhost:5001/data', json={
    'symbol': 'AAPL',
    'start': '2024-01-01',
    'end': '2024-12-31',
    'horizon': 30
})

data = response.json()
print(data)
```

### JavaScript
```javascript
fetch('http://localhost:5001/data', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    symbol: 'AAPL',
    start: '2024-01-01',
    end: '2024-12-31',
    horizon: 30
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

## Rate Limiting

A API TwelveData tem limites:
- **Plano Gratuito:** 8 requisições/minuto
- **Plano Básico:** 800 requisições/dia

## Erros Comuns

### 1. API Key Inválida
```json
{
  "error": "Erro: Invalid API key"
}
```
**Solução:** Verifique sua API key no arquivo `.env`

### 2. Ticker Não Encontrado
```json
{
  "error": "Erro: Symbol not found"
}
```
**Solução:** Use um ticker válido (ex: AAPL, TSLA, MSFT)

### 3. Limite de Requisições
```json
{
  "error": "Erro: API rate limit exceeded"
}
```
**Solução:** Aguarde 1 minuto antes de fazer nova requisição