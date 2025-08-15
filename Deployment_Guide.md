

# StockERP Deployment Guide

## 1. MariaDB Installation

### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install mariadb-server
sudo mysql_secure_installation
sudo mysql -u root -p -e "CREATE DATABASE stockerp;"
sudo mysql -u root -p -e "CREATE USER 'stockerp_user'@'localhost' IDENTIFIED BY 'your_password';"
sudo mysql -u root -p -e "GRANT ALL PRIVILEGES ON stockerp.* TO 'stockerp_user'@'localhost';"
sudo mysql -u root -p -e "FLUSH PRIVILEGES;"
```

### CentOS/RHEL:
```bash
sudo curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
sudo yum install MariaDB-server
sudo systemctl start mariadb
sudo systemctl enable mariadb
sudo mysql_secure_installation
sudo mysql -u root -p -e "CREATE DATABASE stockerp;"
sudo mysql -u root -p -e "CREATE USER 'stockerp_user'@'localhost' IDENTIFIED BY 'your_password';"
sudo mysql -u root -p -e "GRANT ALL PRIVILEGES ON stockerp.* TO 'stockerp_user'@'localhost';"
sudo mysql -u root -p -e "FLUSH PRIVILEGES;"
```

## 2. Service Startup Procedures

### Required Services:
| Service | File | Command | Purpose |
|---------|------|---------|---------|
| API Server | `app.py` | `python app.py` | Backend API for stock data |
| Dashboard | `dashboard.py` | `python dashboard.py` | Visualization frontend |
| Data Sync | `sync_stock_data.py` | `python sync_stock_data.py` | Background data synchronization |

### Startup Script (`start_services.sh`):
```bash
#!/bin/bash

# Start API server
python app.py > api.log 2>&1 &

# Start dashboard
python dashboard.py > dashboard.log 2>&1 &

# Start data sync service
python sync_stock_data.py > sync.log 2>&1 &

echo "All services started. Check logs for details."
```

Make executable:
```bash
chmod +x start_services.sh
```

## 3. Configuration

### .env File:
```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=stockerp
DB_USER=stockerp_user
DB_PASSWORD=your_password
```

### First-Time Setup:
```bash
python setup_db.py        # Initialize database tables
python sync_stock_data.py # Perform initial data sync
```

## 4. Verification Steps

### Check Database:
```bash
mysql -u stockerp_user -p stockerp -e "SELECT COUNT(*) FROM stock_data;"
```

### Test API:
```bash
curl http://localhost:58643/api/stocks/AAPL?period=1y
```

### Access Dashboard:
Open in browser: `http://localhost:52643?symbol=AAPL`

## 5. Production Deployment

### Systemd Service Files:
Create `/etc/systemd/system/stockerp.service`:
```ini
[Unit]
Description=StockERP Service
After=network.target

[Service]
User=stockerp
WorkingDirectory=/opt/stockerp
ExecStart=/usr/bin/python /opt/stockerp/start_services.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

### Start Service:
```bash
sudo systemctl daemon-reload
sudo systemctl start stockerp
sudo systemctl enable stockerp
```

## 6. ERPNext Integration
Follow instructions in `ERPNext_Installation.md` to install the custom app.
