
import schedule
import time
import sqlite3
import pandas as pd
from stock_doctype import Stock

DB_PATH = '/workspace/stockerp/stock_data.db'

def sync_to_db(symbol):
    """Sync stock data to database"""
    try:
        # Fetch data from OpenBB
        data = Stock.get_timeseries_data(symbol, period='max')
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Insert records
        for record in data:
            cursor.execute("""
            INSERT OR IGNORE INTO stock_data (symbol, date, price, volume)
            VALUES (?, ?, ?, ?)
            """, (symbol, record['date'], record['price'], record['volume']))
        
        conn.commit()
        print(f"Synced {len(data)} records for {symbol}")
    except Exception as e:
        print(f"Sync failed for {symbol}: {str(e)}")
    finally:
        conn.close()

if __name__ == '__main__':
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
