from erpnext_client import ERPNextClient
from datetime import datetime, timedelta

class Stock:
    """Interface to ERPNext Stock Doctype"""
    @staticmethod
    def get_timeseries_data(symbol, period='max'):
        """Fetch stock timeseries data from ERPNext"""
        client = ERPNextClient()
        return client.get_stock_data(symbol, period)
    
    @staticmethod
    def _calculate_start_date(period):
        """Calculate start date based on period string"""
        period_map = {
            '1d': 1, '5d': 5, '1mo': 30,
            '3mo': 90, '6mo': 180, '1y': 365,
            '2y': 730, '5y': 1825
        }
        days = period_map.get(period, 365)
        return datetime.now() - timedelta(days=days)
