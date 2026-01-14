import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestIndicadores(unittest.TestCase):
    
    def setUp(self):
       
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)
        
    
        prices = []
        price = 100
        for _ in range(len(dates)):
            change = np.random.normal(0, 0.02)  
            price *= (1 + change)
            prices.append(price)
        
        self.test_data = pd.DataFrame({
            'Open': [p * np.random.uniform(0.98, 1.02) for p in prices],
            'High': [p * np.random.uniform(1.00, 1.05) for p in prices],
            'Low': [p * np.random.uniform(0.95, 1.00) for p in prices],
            'Close': prices,
            'Volume': [np.random.randint(1000000, 10000000) for _ in prices]
        }, index=dates)
    
    def test_sma_calculation(self):
        
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
        
        self.assertIn('SMA_20', result.columns)
        self.assertIn('SMA_50', result.columns)
        
        
        self.assertTrue(result['SMA_20'].iloc[-1] > 0)
        self.assertTrue(result['SMA_50'].iloc[-1] > 0)
        
        
        sma20_std = result['SMA_20'].std()
        sma50_std = result['SMA_50'].std()
        self.assertGreater(sma20_std, sma50_std)
    
    def test_rsi_calculation(self):
       
        from Iqbraq import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
       
        self.assertIn('RSI', result.columns)
        
        
        rsi_values = result['RSI'].dropna()
        self.assertTrue(all(0 <= val <= 100 for val in rsi_values))
    
    def test_macd_calculation(self):
        
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
        
        self.assertIn('MACD', result.columns)
        self.assertIn('MACD_Signal', result.columns)
        
      
        self.assertFalse(result['MACD'].iloc[-1] is None)
        self.assertFalse(result['MACD_Signal'].iloc[-1] is None)
    
    def test_bollinger_bands(self):
        
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
       
        self.assertIn('Upper_Band', result.columns)
        self.assertIn('Lower_Band', result.columns)
        self.assertIn('Middle_Band', result.columns)
        
      
        upper = result['Upper_Band'].iloc[-1]
        lower = result['Lower_Band'].iloc[-1]
        self.assertGreater(upper, lower)

class TestPrevisao(unittest.TestCase):
    
    def setUp(self):
        
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)
        
        
        trend = np.linspace(100, 150, len(dates))
        noise = np.random.normal(0, 5, len(dates))
        prices = trend + noise
        
        self.test_data = pd.DataFrame({
            'Open': prices * 0.99,
            'High': prices * 1.02,
            'Low': prices * 0.98,
            'Close': prices,
            'Volume': [np.random.randint(1000000, 10000000) for _ in prices]
        }, index=dates)
    
    def test_prediction_function(self):
     
        from Iqbraq import prever_precos
        
        df_with_preds, future_df = prever_precos(self.test_data, dias_a_frente=30)
        
        
        self.assertIn('Pred', df_with_preds.columns)
        
       
        self.assertEqual(len(future_df), 30)
        self.assertIn('Date', future_df.columns)
        self.assertIn('Pred', future_df.columns)
        
      
        last_historical = df_with_preds.index.max()
        first_future = pd.to_datetime(future_df['Date'].iloc[0])
        self.assertGreater(first_future, last_historical)

if __name__ == '__main__':
    unittest.main()