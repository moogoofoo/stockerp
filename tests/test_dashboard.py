import pytest
import os
import sys
# ensure project src directory is on the path
topdir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if topdir not in sys.path:
    sys.path.insert(0, topdir)

from dashboard import update_chart

class DummyResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data

def test_update_chart(monkeypatch):
    # Provide dummy JSON
    dummy = {
        'timeseries': [
            {'date': '2025-01-01', 'price': 100.0, 'volume': 1000},
            {'date': '2025-01-02', 'price': 110.0, 'volume': 1050}
        ],
        'period': '1d'
    }
    monkeypatch.setattr('dashboard.requests.get', lambda url: DummyResponse(dummy))
    opt = update_chart(0, '?symbol=TEST', '1d')
    assert 'series' in opt
    assert opt['title']['text'].startswith('TEST')
    assert len(opt['series'][0]['data']) == 2
