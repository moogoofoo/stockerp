

import sqlite3

def initialize_database():
    """Create database tables if they don't exist"""
    conn = sqlite3.connect('/workspace/stockerp/stock_data.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        volume BIGINT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(symbol, date)  -- Prevent duplicate entries
    )
    """)
    
    # Create index for faster symbol-based queries
    cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_symbol 
    ON stock_data (symbol)
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    initialize_database()

