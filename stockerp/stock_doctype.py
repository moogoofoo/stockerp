

from openbb import obb
import pandas as pd

class Stock:
    @staticmethod
    def get_timeseries_data(symbol, period="1y"):
        try:
            # Fetch historical data from OpenBB
            data = obb.equity.price.historical(symbol, provider="yfinance", period=period)
            df = data.to_df()
            
            # Format for frontend
            return [
                {
                    "date": str(idx) if isinstance(idx, pd.Timestamp) else str(idx),
                    "price": row['close'],
                    "volume": row['volume']
                }
                for idx, row in df.iterrows()
            ]
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

