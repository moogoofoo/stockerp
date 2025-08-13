import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Database configuration
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'stockerp')
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API server configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 58643))
API_URL = os.getenv('API_URL', f"http://localhost:{API_PORT}")

# Dashboard server configuration
DASH_HOST = os.getenv('DASH_HOST', '0.0.0.0')
DASH_PORT = int(os.getenv('DASH_PORT', 52643))

# ERPNext credentials
ERPNEXT_API_KEY = os.getenv('ERPNEXT_API_KEY')
ERPNEXT_API_SECRET = os.getenv('ERPNEXT_API_SECRET')
ERPNEXT_URL = os.getenv('ERPNEXT_URL')
