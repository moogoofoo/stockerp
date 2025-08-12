


import os
from dotenv import load_dotenv
from core.database import get_engine

# Load environment variables
load_dotenv()

# Print environment variables
print(f"DB_USER: {os.getenv('DB_USER', 'root')}")
print(f"DB_HOST: {os.getenv('DB_HOST', 'localhost')}")
print(f"DB_NAME: {os.getenv('DB_NAME', 'stockerp')}")

# Test database connection
try:
    engine = get_engine()
    with engine.connect() as connection:
        print("Database connection successful!")
        print(f"Engine: {engine}")
except Exception as e:
    print(f"Database connection failed: {str(e)}")


