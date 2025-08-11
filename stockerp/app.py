


from flask import Flask, jsonify
from stock_doctype import Stock
import random
from datetime import datetime, timedelta

app = Flask(__name__)

# Initialize sample stock
aapl = Stock("AAPL", "Apple Inc.")

# Generate sample timeseries data
start_date = datetime.now() - timedelta(days=30)
for i in range(30):
    date = start_date + timedelta(days=i)
    price = round(150 + random.uniform(-5, 5), 2)
    volume = random.randint(1000000, 5000000)
    aapl.add_price_point(date.isoformat(), price, volume)

@app.route('/api/stocks')
def get_stocks():
    return jsonify({
        "symbol": aapl.symbol,
        "name": aapl.name,
        "timeseries": aapl.get_timeseries_data()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58643)


