from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import io
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('TWELVE_API_KEY')

app = Flask(__name__, static_folder='static', template_folder='templates')



# BAIXAR DADOS DA API

def baixar_dados(ticker, start, end):
    url = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": ticker,
        "interval": "1day",
        "apikey": API_KEY,
        "start_date": start,
        "end_date": end,
        "format": "JSON",
        "outputsize": 5000
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "status" in data and data["status"] == "error":
        print("Erro da API:", data["message"])
        return None

    if "values" not in data:
        print("Resposta inválida:", data)
        return None

    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.sort_values("datetime", inplace=True)

    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
        "datetime": "Date"
    }, inplace=True)

    df.set_index("Date", inplace=True)
    return df



# INDICADORES

def calcular_indicadores(df):
    df = df.copy()

    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()

    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    delta = df['Close'].diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    media_ganho = ganho.rolling(window=14).mean()
    media_perda = perda.rolling(window=14).mean()
    rs = media_ganho / media_perda
    df['RSI'] = 100 - (100 / (1 + rs))

    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    df['Middle_Band'] = df['Close'].rolling(window=20).mean()
    std = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['Middle_Band'] + (2 * std)
    df['Lower_Band'] = df['Middle_Band'] - (2 * std)

    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR_14'] = tr.rolling(window=14).mean()

    obv = [0]
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i - 1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i - 1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv

    return df


# PREVISÃO

def prever_precos(df, dias_a_frente=30, grau=3):
    df = df.copy()
    df.index = pd.to_datetime(df.index)

    dias = (df.index - df.index.min()).days.values.reshape(-1, 1)
    y = df['Close'].values

    modelo = make_pipeline(PolynomialFeatures(degree=grau), LinearRegression())
    modelo.fit(dias, y)

    df['Pred'] = modelo.predict(dias)

    last_day = df.index.max()
    future_dates = [last_day + dt.timedelta(days=i) for i in range(1, dias_a_frente + 1)]
    future_days = np.array([(d - df.index.min()).days for d in future_dates]).reshape(-1, 1)

    future_preds = modelo.predict(future_days)

    future_df = pd.DataFrame({
        'Date': future_dates,
        'Pred': future_preds
    })

    return df, future_df



# ROTAS

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['POST'])
def get_data():
    try:
        payload = request.get_json()
        print(f"Payload recebido: {payload}")
        print(f"API_KEY: {API_KEY}")
        
        symbol = payload.get("symbol", "AAPL")
        start = payload.get("start")
        end = payload.get("end")
        horizon = int(payload.get("horizon", 30))
        
        print(f"Parâmetros: symbol={symbol}, start={start}, end={end}, horizon={horizon}")

        # Baixar dados históricos
        df = baixar_dados(symbol, start, end)
        if df is None:
            return jsonify({"error": "Erro ao baixar dados do ticker"}), 400

        # Calcular indicadores
        df = calcular_indicadores(df)
        
        # Fazer previsão
        df_with_preds, future_df = prever_precos(df, horizon)

        # Preparar dados para o frontend
        candles = []
        for idx, row in df_with_preds.iterrows():
            candles.append({
                "Date": idx.strftime("%Y-%m-%d"),
                "Open": float(row["Open"]),
                "High": float(row["High"]),
                "Low": float(row["Low"]),
                "Close": float(row["Close"]),
                "Volume": int(row["Volume"]),
                "SMA_20": float(row["SMA_20"]) if pd.notna(row["SMA_20"]) else None,
                "SMA_50": float(row["SMA_50"]) if pd.notna(row["SMA_50"]) else None,
                "EMA_12": float(row["EMA_12"]) if pd.notna(row["EMA_12"]) else None,
                "EMA_26": float(row["EMA_26"]) if pd.notna(row["EMA_26"]) else None,
                "RSI": float(row["RSI"]) if pd.notna(row["RSI"]) else None,
                "MACD": float(row["MACD"]) if pd.notna(row["MACD"]) else None,
                "MACD_Signal": float(row["MACD_Signal"]) if pd.notna(row["MACD_Signal"]) else None,
                "Upper_Band": float(row["Upper_Band"]) if pd.notna(row["Upper_Band"]) else None,
                "Lower_Band": float(row["Lower_Band"]) if pd.notna(row["Lower_Band"]) else None,
                "Pred": float(row["Pred"]) if pd.notna(row["Pred"]) else None
            })

        future_data = []
        for idx, row in future_df.iterrows():
            future_data.append({
                "Date": row["Date"].strftime("%Y-%m-%d"),
                "Pred": float(row["Pred"])
            })

        return jsonify({
            "status": "ok",
            "meta": {
                "symbol": symbol,
                "name": f"{symbol} Stock",
                "horizon": horizon
            },
            "candles": candles,
            "data": candles,  # Para compatibilidade
            "future": future_data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/download', methods=['POST'])
def download():
    payload = request.get_json(force=True)
    ticker = payload.get('ticker', '').upper().strip()
    start = payload.get('start')
    end = payload.get('end')
    horizon = int(payload.get('horizon', 30))

    df = baixar_dados(ticker, start, end)
    if df is None:
        return jsonify({'error': 'Ticker inválido.'}), 404

    df = calcular_indicadores(df)
    df_with_preds, future_df = prever_precos(df, horizon)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_with_preds.to_excel(writer, sheet_name='historico')
        future_df.to_excel(writer, sheet_name='previsao_futura', index=False)

    output.seek(0)
    filename = f"{ticker}_data.xlsx"
    return send_file(output, as_attachment=True, download_name=filename)


if __name__ == '__main__':
    app.run(debug=True)
