


from core.database import db_session
from core.pickle_models import PickledStockData
import pickle
import pandas as pd

# Test database connection and data retrieval
with db_session() as session:
    # Get all stock symbols in database
    symbols = [record.symbol for record in session.query(PickledStockData.symbol).distinct()]
    print(f"Stored symbols: {symbols}")
    
    # Retrieve and inspect AAPL data
    aapl_record = session.query(PickledStockData).filter_by(symbol='AAPL').first()
    if aapl_record:
        df = pickle.loads(aapl_record.data_frame)
        print(f"\nAAPL data ({len(df)} records):")
        print(df.head())
    else:
        print("No AAPL data found")


