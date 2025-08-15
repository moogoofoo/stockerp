"""
Utility functions for time period calculations.
"""
from datetime import datetime, timedelta

# Mapping of period codes to days
_PERIOD_DAYS = {
    '1d': 1,
    '5d': 5,
    '1mo': 30,
    '3mo': 90,
    '6mo': 180,
    '1y': 365,
    '2y': 730,
    '5y': 1825,
}


def calculate_start_date(period: str) -> datetime | None:
    """
    Calculate the start datetime for a given period string.
    Returns None if period is 'max' or unrecognized.
    """
    if period == 'max':
        return None
    days = _PERIOD_DAYS.get(period)
    if days is None:
        return None
    return datetime.now() - timedelta(days=days)
