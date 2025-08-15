from erpnext_client import ERPNextClient

class Stock:
    """Interface to ERPNext Stock Doctype"""
    @staticmethod
    def get_timeseries_data(symbol, period='max'):
        """Fetch stock timeseries data from ERPNext"""
        client = ERPNextClient()
        return client.get_stock_data(symbol, period)
    
