
from datetime import datetime, timedelta
from core.database import db_session
from core.pickle_models import PickledStockData
import pandas as pd
import pickle

def get_stock_data_from_db(symbol, period='max'):
    """Fetch stock data from database as DataFrame"""
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
        with db_session() as session:
            # Query pickled data for the symbol
            result = session.query(PickledStockData).filter_by(symbol=symbol).first()
            
            if result:
                # Unpickle DataFrame
                df = pickle.loads(result.data_frame)
                
                # Filter by period if needed
                if time_delta:
                    cutoff_date = datetime.now() - time_delta
                    df = df[df['date'] >= cutoff_date]
                
                # Convert to list of dicts
                return df[['date', 'price', 'volume']].to_dict('records')
            return None
    except Exception as e:
        print(f"Error retrieving stock data: {str(e)}")
        return None
