

from sqlalchemy import Column, String, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockData(Base):
    """Stock data timeseries model"""
    __tablename__ = 'stock_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    
    __table_args__ = (
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )

