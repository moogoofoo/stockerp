


from flask import Flask, jsonify, request
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from get_stock_data import get_stock_data_from_db  # Updated import

load_dotenv()  # Load environment variables

app = Flask(__name__)

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


