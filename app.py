


from flask import Flask, jsonify, request
from flask_cors import CORS
from get_stock_data import get_stock_data_from_db
from config import API_HOST, API_PORT

app = Flask(__name__)
# Enable CORS for API routes
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/stocks/<symbol>')
def get_stock_data(symbol):
    period = request.args.get('period', '1y')
    data = get_stock_data_from_db(symbol, period) or []
    return jsonify({
        "symbol": symbol,
        "period": period,
        "timeseries": data
    })

if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT)


