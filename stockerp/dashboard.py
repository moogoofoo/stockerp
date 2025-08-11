


import dash
from dash import html, dcc
import dash_echarts
import requests
from datetime import datetime

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Interval(id='interval', interval=60*1000, n_intervals=0),
    dash_echarts.DashECharts(
        id='stock-chart',
        style={'width': '100%', 'height': '600px'}
    )
])

@app.callback(
    dash.dependencies.Output('stock-chart', 'option'),
    [dash.dependencies.Input('interval', 'n_intervals')]
)
def update_chart(n):
    try:
        response = requests.get('http://localhost:58643/api/stocks')
        stock_data = response.json()['timeseries']
        
        # Prepare data for ECharts
        dates = [datetime.fromisoformat(point['timestamp']).strftime('%Y-%m-%d') for point in stock_data]
        prices = [point['price'] for point in stock_data]
        volumes = [point['volume'] for point in stock_data]
        
        option = {
            'title': {'text': f'{stock_data[0]["symbol"]} Stock Price History'},
            'tooltip': {'trigger': 'axis'},
            'legend': {'data': ['Price', 'Volume']},
            'xAxis': {
                'type': 'category',
                'data': dates,
                'axisPointer': {'type': 'shadow'}
            },
            'yAxis': [
                {'type': 'value', 'name': 'Price'},
                {'type': 'value', 'name': 'Volume'}
            ],
            'series': [
                {
                    'name': 'Price',
                    'type': 'line',
                    'smooth': True,
                    'data': prices
                },
                {
                    'name': 'Volume',
                    'type': 'bar',
                    'yAxisIndex': 1,
                    'data': volumes
                }
            ]
        }
        return option
    except Exception as e:
        print(f"Error updating chart: {e}")
        return {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=52643, debug=True)


