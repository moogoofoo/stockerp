


import pandas as pd
from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PickledStockData(Base):
    """Model for storing pickled stock DataFrames"""
    __tablename__ = 'pickled_stock_data'
    
    symbol = Column(String(10), primary_key=True)
    data_frame = Column(LargeBinary, nullable=False)  # Stores pickled DataFrame
    
    def get_dataframe(self):
        """Unpickle and return DataFrame"""
        return pd.read_pickle(self.data_frame) if self.data_frame else None


