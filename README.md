# StockERP - ERPNext Stock Timeseries Dashboard

StockERP extends ERPNext with timeseries stock visualization using Dash and dash-echarts.

## Features
- Real-time stock data visualization
- Historical price tracking
- Customizable time periods
- Embedded in ERPNext UI
- MariaDB backend
- Automated data synchronization

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- MariaDB server
- Node.js 16+ (for ERPNext)
- Redis

### 2. Clone Repository
```bash
git clone https://github.com/moogoofoo/stockerp.git
cd stockerp
```

### 3. Create Virtual Environment
```bash
python3.12 -m venv .venv
source .venv/bin/activate 
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Database Setup
1. Create MariaDB database:
```sql
CREATE DATABASE stockerp;
CREATE USER 'stockerp'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON stockerp.* TO 'stockerp'@'localhost';
FLUSH PRIVILEGES;
```

2. Update `.env` file:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=stockerp
DB_USER=stockerp
DB_PASSWORD=your_password
```

3. Initialize database:
```bash
python setup_db.py
```

### 6. Install ERPNext
Follow official ERPNext installation guide:
https://github.com/frappe/frappe_docker

### 7. Install StockERP App in ERPNext
1. Place the `stock_doctype.py` in your ERPNext app directory
2. Add to `hooks.py`:
```python
doctype_js = {
    "Stock": "public/js/stock.js"
}
```

### 8. Start Services
```bash
./start_services.sh
```

Services will run on:
- Backend API: http://localhost:58643
- Frontend Dashboard: http://localhost:52643
- Sync Service: Runs in background

### 9. Access Dashboard in ERPNext
1. Navigate to Stock Doctype in ERPNext
2. The dashboard will be embedded in the stock detail view

## Configuration
- Modify `sync_stock_data.py` to change sync frequency
- Edit `dashboard.py` to customize visualization
- Update `app.py` to modify API endpoints

## Troubleshooting
- Check `backend.log` and `frontend.log` for errors
- Verify database connection in `.env`
- Ensure ports 52643/58643 are available
