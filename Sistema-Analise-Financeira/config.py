import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    TWELVE_API_KEY = os.getenv('TWELVE_API_KEY')
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Data Configuration
    DEFAULT_TICKER = 'AAPL'
    DEFAULT_HORIZON = 30
    MAX_HORIZON = 365
    
    # Cache Configuration
    CACHE_TIMEOUT = 300  # 5 minutes
    
    # Rate Limiting
    RATE_LIMIT = "100/hour"
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.TWELVE_API_KEY:
            raise ValueError("TWELVE_API_KEY environment variable is required")
        return True