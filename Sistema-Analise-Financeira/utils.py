import logging
import sys
from functools import wraps
from flask import jsonify

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def handle_api_errors(f):
    """Decorator to handle API errors consistently"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            logging.error(f"Validation error: {str(e)}")
            return jsonify({'error': f'Validation error: {str(e)}'}), 400
        except ConnectionError as e:
            logging.error(f"Connection error: {str(e)}")
            return jsonify({'error': 'Unable to connect to data provider'}), 503
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function

class APIError(Exception):
    """Custom API Error class"""
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)