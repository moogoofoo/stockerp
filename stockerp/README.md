
# StockERP Dashboard

ERPNext integration for visualizing stock timeseries data using Dash and dash-echarts.

## Features
- Embedded dash-echarts in ERPNext stock views
- Real-time stock data visualization
- Custom ERPNext app for seamless integration
- Dual-axis charts (price + volume)

## Installation
```bash
bench get-app stock_dashboard https://github.com/moogoofoo/stockerp/tree/stock-dashboard-demo
bench install-app stock_dashboard
bench restart
```

## Configuration
1. Start the Dash server:
   ```bash
   cd /path/to/stockerp
   python dashboard.py
   ```
2. Access in ERPNext at: `/stock_dashboard?symbol=AAPL`

