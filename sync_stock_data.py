
import schedule
import time
import mariadb
import os
from dotenv import load_dotenv
import pandas as pd
from stock_doctype import Stock

from setup_db import initialize_database  # Add database initialization
load_dotenv()  # Load environment variables

def sync_to_db(symbol):
    """Sync stock data to MariaDB database"""
    try:
        # Fetch data from OpenBB
        data = Stock.get_timeseries_data(symbol, period='max')
        
        # Connect to MariaDB
        conn = mariadb.connect(
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            database=os.getenv('DB_NAME', 'stockerp')
        )
        cursor = conn.cursor()
        
        # Insert records
        for record in data:
            cursor.execute("""
            INSERT IGNORE INTO stock_data (symbol, date, price, volume)
            VALUES (?, ?, ?, ?)
            """, (symbol, record['date'], record['price'], record['volume']))
        
        conn.commit()
        print(f"Synced {len(data)} records for {symbol}")
    except Exception as e:
        print(f"Sync failed for {symbol}: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
    # Initialize database before first sync
    initialize_database()
    
    # Initial sync for popular symbols
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    for symbol in symbols:
        sync_to_db(symbol)
    
    # Schedule daily sync at 9:30 AM market open
    schedule.every().day.at("09:30").do(
        lambda: [sync_to_db(s) for s in symbols]
    )
    
    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)
