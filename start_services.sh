
#!/bin/bash

# Start API server
python app.py > api.log 2>&1 &

# Start dashboard
python dashboard.py > dashboard.log 2>&1 &

# Start data sync service
python sync_stock_data.py > sync.log 2>&1 &

echo "All services started. Check logs:"
echo " - API: api.log"
echo " - Dashboard: dashboard.log"
echo " - Sync: sync.log"
