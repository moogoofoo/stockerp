

import mariadb
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

def initialize_database():
    """Create database tables in MariaDB if they don't exist"""
    try:
        conn = mariadb.connect(
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            database=os.getenv('DB_NAME', 'stockerp')
        )
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            volume BIGINT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE(symbol, date)
        """)
        
        # Create index for faster symbol-based queries
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_symbol 
        ON stock_data (symbol)
        """)
        
        conn.commit()
        print("MariaDB database initialized successfully!")
    except mariadb.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    initialize_database()

