import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestIndicadores(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)
        
        # Generate realistic stock data
        prices = []
        price = 100
        for _ in range(len(dates)):
            change = np.random.normal(0, 0.02)  # 2% daily volatility
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
        """Test Simple Moving Average calculation"""
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
        # Check if SMA columns exist
        self.assertIn('SMA_20', result.columns)
        self.assertIn('SMA_50', result.columns)
        
        # Check if SMA values are reasonable
        self.assertTrue(result['SMA_20'].iloc[-1] > 0)
        self.assertTrue(result['SMA_50'].iloc[-1] > 0)
        
        # SMA_20 should be more responsive than SMA_50
        sma20_std = result['SMA_20'].std()
        sma50_std = result['SMA_50'].std()
        self.assertGreater(sma20_std, sma50_std)
    
    def test_rsi_calculation(self):
        """Test RSI calculation"""
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
        # Check if RSI column exists
        self.assertIn('RSI', result.columns)
        
        # RSI should be between 0 and 100
        rsi_values = result['RSI'].dropna()
        self.assertTrue(all(0 <= val <= 100 for val in rsi_values))
    
    def test_macd_calculation(self):
        """Test MACD calculation"""
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
        # Check if MACD columns exist
        self.assertIn('MACD', result.columns)
        self.assertIn('MACD_Signal', result.columns)
        
        # MACD values should exist
        self.assertFalse(result['MACD'].iloc[-1] is None)
        self.assertFalse(result['MACD_Signal'].iloc[-1] is None)
    
    def test_bollinger_bands(self):
        """Test Bollinger Bands calculation"""
        from sistema_analise_financeira import calcular_indicadores
        
        result = calcular_indicadores(self.test_data)
        
        # Check if Bollinger Bands columns exist
        self.assertIn('Upper_Band', result.columns)
        self.assertIn('Lower_Band', result.columns)
        self.assertIn('Middle_Band', result.columns)
        
        # Upper band should be greater than lower band
        upper = result['Upper_Band'].iloc[-1]
        lower = result['Lower_Band'].iloc[-1]
        self.assertGreater(upper, lower)

class TestPrevisao(unittest.TestCase):
    
    def setUp(self):
        """Set up test data for prediction"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)
        
        # Generate trend data for better prediction testing
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
        """Test price prediction function"""
        from sistema_analise_financeira import prever_precos
        
        df_with_preds, future_df = prever_precos(self.test_data, dias_a_frente=30)
        
        # Check if prediction columns exist
        self.assertIn('Pred', df_with_preds.columns)
        
        # Check future predictions
        self.assertEqual(len(future_df), 30)
        self.assertIn('Date', future_df.columns)
        self.assertIn('Pred', future_df.columns)
        
        # Future dates should be after the last historical date
        last_historical = df_with_preds.index.max()
        first_future = pd.to_datetime(future_df['Date'].iloc[0])
        self.assertGreater(first_future, last_historical)

if __name__ == '__main__':
    unittest.main()