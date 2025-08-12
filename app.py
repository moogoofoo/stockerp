from flask import Flask, jsonify, request
import mariadb
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__)

def get_stock_data_from_db(symbol, period):
    """Fetch stock data from MariaDB database"""
    # Map period to time delta
    period_map = {
        '1d': timedelta(days=1),
        '5d': timedelta(days=5),
        '1mo': timedelta(days=30),
        '3mo': timedelta(days=90),
        '6mo': timedelta(days=180),
        '1y': timedelta(days=365),
        '2y': timedelta(days=730),
        '5y': timedelta(days=1825),
        'max': None
    }
    time_delta = period_map.get(period)
    
    try:
        # Connect to MariaDB
        conn = mariadb.connect(
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            database=os.getenv('DB_NAME', 'stockerp')
        )
        cursor = conn.cursor()
        
        # Build query based on period
        if time_delta:
            start_date = datetime.now() - time_delta
            query = """
                SELECT date, price, volume 
                FROM stock_data 
                WHERE symbol = ? AND date >= ?
                ORDER BY date
            """
            cursor.execute(query, (symbol, start_date.strftime('%Y-%m-%d')))
        else:
            query = """
                SELECT date, price, volume 
                FROM stock_data 
                WHERE symbol = ? 
                ORDER BY date
            """
            cursor.execute(query, (symbol,))
        
        # Format results
        data = []
        for row in cursor.fetchall():
            data.append({
                'date': row[0].strftime('%Y-%m-%d'),
                'price': float(row[1]),
                'volume': int(row[2])
            })
        return data
    except mariadb.Error as e:
        return {'error': f'Database error: {e}'}
    finally:
        if conn:
            conn.close()

@app.route('/api/stocks/<symbol>')
def get_stock_data(symbol):
    period = request.args.get('period', '1y')
    data = get_stock_data_from_db(symbol, period)
    return jsonify({
        "symbol": symbol,
        "period": period,
        "timeseries": data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58643)
