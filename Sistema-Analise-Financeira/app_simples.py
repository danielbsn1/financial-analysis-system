from flask import Flask, render_template, request, jsonify, send_file
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import io
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

load_dotenv()
API_KEY = os.getenv('TWELVE_API_KEY')

app = Flask(__name__, static_folder='static', template_folder='templates')

def calcular_indicadores(df):
    """Calcula indicadores técnicos reais"""
    # SMA
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()
    
    # EMA
    df['EMA_12'] = df['Close'].ewm(span=12).mean()
    df['EMA_26'] = df['Close'].ewm(span=26).mean()
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
    df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
    
    # Bollinger Bands
    df['Middle_Band'] = df['Close'].rolling(window=20).mean()
    std = df['Close'].rolling(window=20).std()
    df['Upper_Band'] = df['Middle_Band'] + (2 * std)
    df['Lower_Band'] = df['Middle_Band'] - (2 * std)
    
    # ATR (Average True Range)
    high_low = df['High'] - df['Low']
    high_close = (df['High'] - df['Close'].shift()).abs()
    low_close = (df['Low'] - df['Close'].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    df['ATR'] = tr.rolling(window=14).mean()
    
    # Stochastic Oscillator
    low_14 = df['Low'].rolling(window=14).min()
    high_14 = df['High'].rolling(window=14).max()
    df['Stochastic_K'] = 100 * ((df['Close'] - low_14) / (high_14 - low_14))
    df['Stochastic_D'] = df['Stochastic_K'].rolling(window=3).mean()
    
    # OBV (On Balance Volume)
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    df['OBV'] = obv
    
    # Williams %R
    df['Williams_R'] = -100 * ((high_14 - df['Close']) / (high_14 - low_14))
    
    # CCI (Commodity Channel Index)
    tp = (df['High'] + df['Low'] + df['Close']) / 3
    sma_tp = tp.rolling(window=20).mean()
    mad = tp.rolling(window=20).apply(lambda x: np.abs(x - x.mean()).mean())
    df['CCI'] = (tp - sma_tp) / (0.015 * mad)
    
    return df

def prever_precos(df, dias=30):
    """Previsão de preços usando regressão polinomial"""
    df_copy = df.copy()
    df_copy = df_copy.dropna()
    
    # Preparar dados
    X = np.arange(len(df_copy)).reshape(-1, 1)
    y = df_copy['Close'].values
    
    # Modelo de regressão polinomial
    model = make_pipeline(PolynomialFeatures(2), LinearRegression())
    model.fit(X, y)
    
    # Predições in-sample
    df_copy['Pred'] = model.predict(X)
    
    # Predições futuras
    future_X = np.arange(len(df_copy), len(df_copy) + dias).reshape(-1, 1)
    future_preds = model.predict(future_X)
    
    future_dates = []
    last_date = df_copy.index[-1]
    for i in range(1, dias + 1):
        future_dates.append((last_date + timedelta(days=i)).strftime('%Y-%m-%d'))
    
    future_data = [{'Date': date, 'Pred': pred} for date, pred in zip(future_dates, future_preds)]
    
    return df_copy, future_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['POST'])
def get_data():
    try:
        data = request.get_json()
        symbol = data.get('symbol', 'AAPL')
        start = data.get('start')
        end = data.get('end')
        horizon = int(data.get('horizon', 30))
        
        # Buscar dados da API
        url = "https://api.twelvedata.com/time_series"
        params = {
            'symbol': symbol,
            'interval': '1day',
            'apikey': API_KEY,
            'outputsize': 200,
            'start_date': start,
            'end_date': end
        }
        
        response = requests.get(url, params=params)
        api_data = response.json()
        
        if 'values' not in api_data:
            return jsonify({'error': f'Erro: {api_data.get("message", "Dados não encontrados")}'}), 400
            
        # Converter para DataFrame
        df = pd.DataFrame(api_data['values'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.sort_values('datetime')
        df.set_index('datetime', inplace=True)
        
        # Converter colunas para numérico
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
            
        df.rename(columns={
            'open': 'Open', 'high': 'High', 'low': 'Low', 
            'close': 'Close', 'volume': 'Volume'
        }, inplace=True)
        
        # Calcular indicadores
        df = calcular_indicadores(df)
        
        # Fazer previsão
        df_with_pred, future_data = prever_precos(df, horizon)
        
        # Preparar dados para o frontend
        processed_data = []
        for idx, row in df_with_pred.iterrows():
            processed_data.append({
                'Date': idx.strftime('%Y-%m-%d'),
                'Open': float(row['Open']),
                'High': float(row['High']),
                'Low': float(row['Low']),
                'Close': float(row['Close']),
                'Volume': int(row['Volume']),
                'SMA_20': float(row['SMA_20']) if pd.notna(row['SMA_20']) else None,
                'SMA_50': float(row['SMA_50']) if pd.notna(row['SMA_50']) else None,
                'EMA_12': float(row['EMA_12']) if pd.notna(row['EMA_12']) else None,
                'EMA_26': float(row['EMA_26']) if pd.notna(row['EMA_26']) else None,
                'RSI': float(row['RSI']) if pd.notna(row['RSI']) else None,
                'MACD': float(row['MACD']) if pd.notna(row['MACD']) else None,
                'MACD_Signal': float(row['MACD_Signal']) if pd.notna(row['MACD_Signal']) else None,
                'Upper_Band': float(row['Upper_Band']) if pd.notna(row['Upper_Band']) else None,
                'Lower_Band': float(row['Lower_Band']) if pd.notna(row['Lower_Band']) else None,
                'Pred': float(row['Pred']) if pd.notna(row['Pred']) else None
            })
        
        return jsonify({
            'status': 'ok',
            'meta': {
                'symbol': symbol,
                'name': f'{symbol} Stock',
                'horizon': horizon
            },
            'data': processed_data,
            'future': future_data
        })
        
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        symbol = data.get('ticker', 'AAPL')
        start = data.get('start')
        end = data.get('end')
        horizon = int(data.get('horizon', 30))
        
        url = "https://api.twelvedata.com/time_series"
        params = {
            'symbol': symbol,
            'interval': '1day',
            'apikey': API_KEY,
            'outputsize': 200,
            'start_date': start,
            'end_date': end
        }
        
        response = requests.get(url, params=params)
        api_data = response.json()
        
        if 'values' not in api_data:
            return jsonify({'error': 'Dados não encontrados'}), 400
            
        df = pd.DataFrame(api_data['values'])
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.sort_values('datetime')
        df.set_index('datetime', inplace=True)
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
            
        df.rename(columns={
            'open': 'Open', 'high': 'High', 'low': 'Low', 
            'close': 'Close', 'volume': 'Volume'
        }, inplace=True)
        
        df = calcular_indicadores(df)
        df_with_pred, future_df = prever_precos(df, horizon)
        
        # Criar Excel com formatação
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_with_pred.to_excel(writer, sheet_name='Dados_Historicos')
            pd.DataFrame(future_df).to_excel(writer, sheet_name='Previsao_Futura', index=False)
            
            workbook = writer.book
            
            # Formatos
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            money_format = workbook.add_format({'num_format': '$#,##0.00'})
            
            worksheet1 = writer.sheets['Dados_Historicos']
            worksheet1.set_column('A:A', 12)
            worksheet1.set_column('B:Z', 15, money_format)
            
            worksheet2 = writer.sheets['Previsao_Futura']
            worksheet2.set_column('A:A', 12)
            worksheet2.set_column('B:B', 15, money_format)
        
        output.seek(0)
        return send_file(
            output, 
            as_attachment=True, 
            download_name=f'{symbol}_analise_{datetime.now().strftime("%Y%m%d")}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        print(f"Erro no download: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"API Key: {API_KEY[:10]}...")
    app.run(debug=True, port=5001)