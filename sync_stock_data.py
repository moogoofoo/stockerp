from openbb import obb
import schedule
import time
from core.database import db_session
from core.pickle_models import PickledStockData
import pandas as pd
import pickle
import datetime as dt

START_DATE = "1950-01-01"
END_DATE = dt.date.today().isoformat()

def sync_to_db(symbol):
    """Sync entire stock timeseries as pickled DataFrame"""
    try:
        resp = obb.equity.price.historical(
            symbol=symbol,
            start_date=START_DATE,
            end_date=END_DATE,
            provider="yfinance",
            format="json"  # avoid Arrow issues
        )
        df = (
            resp.to_dataframe()
            .reset_index()
            .assign(
                date=lambda d: pd.to_datetime(d["date"]),
                symbol=symbol
            )
            .rename(columns=str.lower)
            .loc[:, ["symbol", "date", "open", "high", "low", "close", "volume"]]
        )
        
        # Add symbol column to DataFrame (already included in mock data)
        
        # Pickle the DataFrame
        pickled_df = pickle.dumps(df)
        
        with db_session() as session:
            # Check if record exists
            existing = session.query(PickledStockData).filter_by(symbol=symbol).first()
            
            if existing:
                # Update existing record
                existing.data_frame = pickled_df
            else:
                # Create new record
                stock_record = PickledStockData(
                    symbol=symbol,
                    data_frame=pickled_df
                )
                session.add(stock_record)
            
            print(f"Synced {len(df)} records for {symbol} as pickled DataFrame")
    except Exception as e:
        print(f"Sync failed for {symbol}: {str(e)}")

if __name__ == '__main__':
    from core.database import get_engine
    from core.pickle_models import Base
    
    # Create tables for pickled data model
    engine = get_engine()
    Base.metadata.create_all(engine)
    
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
