import os
import sys
# ensure project src directory is on the path
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if topdir not in sys.path:
    sys.path.insert(0, topdir)

import pytest
from flask import json

import app

@ pytest.fixture
def client():
    app.app.config['TESTING'] = True
    return app.app.test_client()


def test_get_stock_data_success(monkeypatch, client):
    # Mock the database call to return known data
    sample = [{'date': '2025-08-12', 'price': 150.0, 'volume': 1200}]
    # Patch get_stock_data_from_db in the module where it's imported
    monkeypatch.setattr('app.get_stock_data_from_db', lambda symbol, period: sample)

    response = client.get('/api/stocks/TEST?period=1y')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['symbol'] == 'TEST'
    assert data['period'] == '1y'
    assert data['timeseries'] == sample
