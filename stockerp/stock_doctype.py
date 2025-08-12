from sqlalchemy import create_engine, Column, String, Date, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Create base class for ORM
Base = declarative_base()

class StockData(Base):
    """SQLAlchemy model for stock_data table"""
    __tablename__ = 'stock_data'
    
    symbol = Column(String(10), primary_key=True)
    date = Column(Date, primary_key=True)
    price = Column(Float)
    volume = Column(Integer)

# Database connection setup
def create_db_engine():
    """Create SQLAlchemy engine using environment variables"""
    return create_engine(
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:{os.getenv('DB_PASSWORD', '')}"
        f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', 3306)}"
        f"/{os.getenv('DB_NAME', 'stockerp')}"
    )

# Period mapping configuration
PERIOD_MAP = {
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

def get_timeseries_data(symbol, period):
    """Fetch stock timeseries data using SQLAlchemy ORM"""
    engine = create_db_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        time_delta = PERIOD_MAP.get(period)
        query = session.query(StockData).filter_by(symbol=symbol)
        
        if time_delta:
            start_date = datetime.now() - time_delta
            query = query.filter(StockData.date >= start_date.date())
        
        query = query.order_by(StockData.date)
        
        # Format results
        data = [
            {
                'date': row.date.strftime('%Y-%m-%d'),
                'price': row.price,
                'volume': row.volume
            }
            for row in query.all()
        ]
        
        return data
    except SQLAlchemyError as e:
        return {'error': f'Database error: {str(e)}'}
    finally:
        session.close()
