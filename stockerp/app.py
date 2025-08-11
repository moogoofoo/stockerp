


from flask import Flask, jsonify, request
from stock_doctype import Stock

app = Flask(__name__)

@app.route('/api/stocks/<symbol>')
def get_stock_data(symbol):
    # Get period parameter (default: 1y)
    period = request.args.get('period', '1y')
    
    # Fetch historical data using OpenBB
    data = Stock.get_timeseries_data(symbol, period)
    return jsonify({
        "symbol": symbol,
        "period": period,
        "timeseries": data
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58643)


