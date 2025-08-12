

import requests
import frappeclient
import os
from dotenv import load_dotenv

load_dotenv()

class ERPNextClient:
    def __init__(self):
        self.api_key = os.getenv('ERPNEXT_API_KEY')
        self.api_secret = os.getenv('ERPNEXT_API_SECRET')
        self.base_url = os.getenv('ERPNEXT_URL')
        
        if not all([self.api_key, self.api_secret, self.base_url]):
            raise ValueError("Missing ERPNext credentials in environment variables")
        
        self.client = frappeclient.FrappeClient(
            url=self.base_url,
            api_key=self.api_key,
            api_secret=self.api_secret
        )
    
    def get_stock_data(self, symbol, period='max'):
        """Fetch stock timeseries data from ERPNext Stock Doctype"""
        filters = [['symbol', '=', symbol]]
        fields = ['date', 'price', 'volume']
        
        if period != 'max':
            # Add date filtering based on period
            filters.append(['date', '>=', self._calculate_start_date(period)])
        
        return self.client.get_list(
            'Stock',
            filters=filters,
            fields=fields,
            order_by='date'
        )
    
    def _calculate_start_date(self, period):
        """Calculate start date based on period string"""
        period_map = {
            '1d': 1, '5d': 5, '1mo': 30,
            '3mo': 90, '6mo': 180, '1y': 365,
            '2y': 730, '5y': 1825
        }
        days = period_map.get(period, 365)
        return datetime.now() - timedelta(days=days)

