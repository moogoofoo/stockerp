

class Stock:
    def __init__(self, symbol, name):
        self.symbol = symbol
        self.name = name
        self.historical_data = []
        
    def add_price_point(self, timestamp, price, volume):
        self.historical_data.append({
            'timestamp': timestamp,
            'price': price,
            'volume': volume
        })
        
    def get_timeseries_data(self):
        return self.historical_data

