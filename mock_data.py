


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_mock_stock_data(symbol, days=365):
    """Generate mock stock data for testing"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    dates = pd.date_range(start_date, end_date, freq='D')
    base_price = random.uniform(50, 200)
    volatility = random.uniform(0.5, 2.0)
    
    prices = []
    for i in range(len(dates)):
        price = base_price * (1 + volatility * np.random.normal(0, 0.01))
        prices.append(round(price, 2))
    
    volumes = [random.randint(10000, 1000000) for _ in range(len(dates))]
    
    return pd.DataFrame({
        'date': dates,
        'price': prices,
        'volume': volumes,
        'symbol': symbol
    })


