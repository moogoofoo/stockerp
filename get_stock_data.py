import logging
import pickle
from core.database import db_session
from core.pickle_models import PickledStockData
from core.utils import calculate_start_date

logger = logging.getLogger(__name__)

def get_stock_data_from_db(symbol: str, period: str = 'max') -> list[dict] | None:
    """
    Fetch stock data from database as list of dicts.
    Applies period filtering using calculate_start_date.
    Returns None on error or if no data found.
    """
    start_date = calculate_start_date(period)
    try:
        with db_session() as session:
            record = session.query(PickledStockData).filter_by(symbol=symbol).first()
            if not record or not record.data_frame:
                return None
            # Unpickle DataFrame
            df = pickle.loads(record.data_frame)
            # Filter by period if needed
            if start_date:
                df = df[df['date'] >= start_date]
            # Convert dates to strings for JSON serialization
            df['date'] = df['date'].dt.strftime('%Y-%m-%d')
            # Return list of dicts
            return df[['date', 'price', 'volume']].to_dict('records')
    except Exception:
        logger.exception(f"Error retrieving stock data for {symbol} period {period}")
        return None
