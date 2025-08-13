
from openbb import obb
import schedule
import time
from core.database import db_session, get_engine
from core.pickle_models import Base
import pandas as pd
import pickle
import datetime as dt
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

START_DATE = "1950-01-01"
END_DATE = dt.date.today().isoformat()
DEFAULT_TABLE_NAME = 'pickled_stock_data'

def create_stock_data_model(table_name=DEFAULT_TABLE_NAME):
    """Create a dynamic model for stock data with specified table name"""
    CustomBase = declarative_base()
    
    class DynamicStockData(CustomBase):
        """Dynamic model for storing pickled stock DataFrames"""
        __tablename__ = table_name
        
        symbol = Column(String(10), primary_key=True)
        data_frame = Column(LargeBinary, nullable=False)  # Stores pickled DataFrame
        
        def get_dataframe(self):
            """Unpickle and return DataFrame"""
            return pickle.loads(self.data_frame) if self.data_frame else None
    
    return DynamicStockData, CustomBase

def sync_stock_symbols(symbols, table_name=DEFAULT_TABLE_NAME):
    """Sync stock symbols to specified table name"""
    if not symbols:
        print("No symbols provided to sync")
        return
    
    # Create dynamic model
    StockDataModel, DynamicBase = create_stock_data_model(table_name)
    
    # Create tables
    engine = get_engine()
    DynamicBase.metadata.create_all(engine, tables=[StockDataModel.__table__])
    
    def sync_single_symbol(symbol):
        """Sync a single symbol to the database"""
        try:
            resp = obb.equity.price.historical(
                symbol=symbol,
                start_date=START_DATE,
                end_date=END_DATE,
                provider="yfinance",
                format="json"
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
            
            # Pickle the DataFrame
            pickled_df = pickle.dumps(df)
            
            with db_session() as session:
                # Check if record exists
                existing = session.query(StockDataModel).filter_by(symbol=symbol).first()
                
                if existing:
                    # Update existing record
                    existing.data_frame = pickled_df
                else:
                    # Create new record
                    stock_record = StockDataModel(
                        symbol=symbol,
                        data_frame=pickled_df
                    )
                    session.add(stock_record)
                
                print(f"Synced {len(df)} records for {symbol} in table '{table_name}'")
                return True
                
        except Exception as e:
            print(f"Sync failed for {symbol} in table '{table_name}': {str(e)}")
            return False
    
    # Sync all symbols
    success_count = 0
    for symbol in symbols:
        if sync_single_symbol(symbol):
            success_count += 1
    
    print(f"Sync completed: {success_count}/{len(symbols)} symbols synced to table '{table_name}'")
    return success_count

def main():
    """Main function for command line execution"""
    # Initial sync for popular symbols
    symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    
    # Sync to default table
    sync_stock_symbols(symbols, DEFAULT_TABLE_NAME)
    
    # Schedule daily sync for default table
    schedule.every().day.at("09:30").do(
        lambda: sync_stock_symbols(symbols, DEFAULT_TABLE_NAME)
    )
    
    # Run scheduler
    print("Starting scheduler for default table...")
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()

