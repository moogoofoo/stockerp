import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, BigInteger, TIMESTAMP, Index
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

Base = declarative_base()

class StockData(Base):
    __tablename__ = "stock_data"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    symbol     = Column(String(10), nullable=False)
    date       = Column(Date, nullable=False)
    price      = Column(DECIMAL(10, 2), nullable=False)
    volume     = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")
    updated_at = Column(
        TIMESTAMP,
        server_default="CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
    )

    __table_args__ = (
        Index("idx_symbol", "symbol"),          # composite index
        # Enforce the UNIQUE(symbol, date) constraint
        Index("uq_symbol_date", "symbol", "date", unique=True),
    )

def initialize_database():
    """Create tables via SQLAlchemy if they do not yet exist."""
    db_url = (
        f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
        f"{os.getenv('DB_PASSWORD', '')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', 3306)}/"
        f"{os.getenv('DB_NAME', 'stockerp')}"
    )

    engine = create_engine(db_url, echo=False, pool_pre_ping=True)
    try:
        Base.metadata.create_all(engine)
        print("MariaDB database initialized successfully with SQLAlchemy!")
    except Exception as e:
        print(f"Database initialization error: {e}")

if __name__ == "__main__":
    initialize_database()
