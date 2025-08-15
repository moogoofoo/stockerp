
# StockERP Repository Summary

## Purpose
StockERP is an extension for ERPNext that provides real-time stock timeseries visualization and dashboard capabilities. It integrates with ERPNext to display historical stock data, price tracking, and customizable time period analysis using Dash and dash-echarts for interactive visualizations.

## General Setup
- **Backend**: Flask-based REST API with SQLAlchemy ORM
- **Frontend**: Dash dashboard with dash-echarts for interactive charts
- **Database**: MariaDB/MySQL backend for storing stock timeseries data
- **Integration**: ERPNext custom app integration with embedded dashboard views
- **Sync**: Automated background synchronization service for stock data updates

## Repository Structure
```
stockerp/
├── app.py                 # Flask REST API endpoints
├── dashboard.py          # Dash dashboard application
├── config.py            # Configuration settings (API host/port)
├── requirements.txt     # Python dependencies
├── core/               # Core business logic
│   ├── database.py     # Database connection and models
│   ├── database_utils.py # Database utility functions
│   ├── pickle_models.py # ML model serialization
│   └── utils.py        # General utility functions
├── tests/              # Test suite
│   ├── test_api.py     # API endpoint tests
│   ├── test_dashboard.py # Dashboard tests
│   ├── test_database.py # Database tests
├── erpnext_client.py   # ERPNext API client
├── get_stock_data.py   # Stock data retrieval
├── sync_stock_data.py  # Background sync service
├── stock_doctype.py    # ERPNext custom doctype
└── start_services.sh   # Service startup script
```

## Development Tools & CI
- **Code Formatting**: Black (>=24.0.0)
- **Linting**: Flake8 (>=7.0.0)
- **Testing**: Pytest (>=7.0.0)
- **Dependencies**: Managed via requirements.txt

## Key Services
- **Backend API**: Runs on configurable port (default: 58643)
- **Frontend Dashboard**: Runs on configurable port (default: 52643)
- **Sync Service**: Background process for data synchronization

## Configuration
Environment variables required:
- DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD for database connection
- API_HOST, API_PORT for Flask API configuration

