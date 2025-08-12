
# ERPNext Integration Guide

## Prerequisites
- ERPNext v14+ installed
- Python 3.10+
- Bench CLI

## Installation Steps
```bash
# Add custom app to your bench
bench get-app stock_dashboard https://github.com/moogoofoo/stockerp

# Install app on site
bench --site yoursite.com install-app stock_dashboard

# Add required dependencies
bench --site yoursite.com pip install openbb pandas

# Set environment variables
bench --site yoursite.com set-config openbb_api_key YOUR_OPENBB_KEY

# Restart ERPNext
bench restart
```

## Configuration
1. Create custom Stock Doctype with fields:
   - symbol (Data)
   - name (Data)
   - last_sync (Datetime)
2. Add dashboard view hook:
   ```python
   def stock_dashboard_view(doc):
       return f"/stock_dashboard?symbol={doc.symbol}"
   ```

## Usage
- Stock dashboard will automatically appear in stock doctype views
- Data syncs daily via cron job
