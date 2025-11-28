from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import io

app = Flask(__name__, static_folder='static', template_folder='templates')


def baixar_dados(ticker, start, end):
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        return None
    return df


def calcular_indicadores(df):
    df = df.copy()

    # EMAs
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()

    # SMAs
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()

    # RSI
    delta = df['Close'].diff()
    ganho = delta.clip(lower=0)
    perda = -delta.clip(upper=0)
    media_ganho = ganho.rolling(window=14).mean()
    media_perda = perda.rolling(window=14).mean()
    rs = media_ganho / media_perda
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    ema_12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema_26 = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = ema_12 - ema_26
    df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

    # Bollinger
    df['Middle_Band'] = df['Close'].rolling(window=20).mean()
    std = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['Middle_Band'] + (2 * std)
    df['Lower_Band'] = df['Middle_Band'] - (2 * std)

    # ATR (Average True Range)
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR_14'] = tr.rolling(window=14).mean()

    # OBV (On Balance Volume)
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


def prever_precos(df, dias_a_frente=30, grau=3):
    """
    Ajusta modelo polinomial no histórico e prevê 'dias_a_frente' dias.
    Retorna df com coluna 'Pred' (predição in-sample) e um DataFrame futuro com datas & previsões.
    """
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    dias = (df.index - df.index.min()).days
    X = dias.reshape(-1, 1)
    y = df['Close'].values

    modelo = make_pipeline(PolynomialFeatures(degree=grau), LinearRegression())
    modelo.fit(X, y)

    in_sample_preds = modelo.predict(X)
    df['Pred'] = in_sample_preds

    last_day = df.index.max()
    future_dates = [last_day + dt.timedelta(days=int(i)) for i in range(1, dias_a_frente + 1)]
    future_days = np.array([(d - df.index.min()).days for d in future_dates]).reshape(-1, 1)
    future_preds = modelo.predict(future_days)

    future_df = pd.DataFrame({
        'Date': future_dates,
        'Pred': future_preds
    })
    future_df['Date'] = future_df['Date'].dt.strftime('%Y-%m-%d')

    return df, future_df


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data', methods=['POST'])
def get_data():
    payload = request.get_json(force=True)
    ticker = payload.get('ticker', '').upper().strip()
    start = payload.get('start')
    end = payload.get('end')
    horizon = int(payload.get('horizon', 30))  # dias futuros: 7/30/60

    if not ticker:
        return jsonify({'error': 'Informe um ticker válido.'}), 400

    try:
        df = baixar_dados(ticker, start, end)
        if df is None:
            return jsonify({'error': 'Ticker inválido ou sem dados no intervalo informado.'}), 404

        df = calcular_indicadores(df)
        df_with_preds, future_df = prever_precos(df, dias_a_frente=horizon, grau=3)

        # Reset index e converter datas em string
        out = df_with_preds.reset_index()
        out['Date'] = out['Date'].dt.strftime('%Y-%m-%d')

        records = out.to_dict(orient='records')
        future_records = future_df.to_dict(orient='records')

        return jsonify({
            'meta': {
                'ticker': ticker,
                'start': start,
                'end': end,
                'horizon': horizon
            },
            'data': records,
            'future': future_records
        })

    except Exception as e:
        return jsonify({'error': f'Erro ao processar: {str(e)}'}), 500


@app.route('/download', methods=['POST'])
def download():
    """
    Recebe os mesmos parâmetros, gera arquivo Excel e retorna para download.
    """
    payload = request.get_json(force=True)
    ticker = payload.get('ticker', '').upper().strip()
    start = payload.get('start')
    end = payload.get('end')
    horizon = int(payload.get('horizon', 30))

    if not ticker:
        return jsonify({'error': 'Informe um ticker válido.'}), 400

    df = baixar_dados(ticker, start, end)
    if df is None:
        return jsonify({'error': 'Ticker inválido ou sem dados no intervalo informado.'}), 404

    df = calcular_indicadores(df)
    df_with_preds, future_df = prever_precos(df, dias_a_frente=horizon, grau=3)

    # Escrever Excel em memória
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_with_preds.to_excel(writer, sheet_name='historico')
        future_df.to_excel(writer, sheet_name='previsao_futura', index=False)
        writer.save()

    output.seek(0)
    filename = f'{ticker}_data_{start}_to_{end}.xlsx'
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


if __name__ == '__main__':
    app.run(debug=True)
