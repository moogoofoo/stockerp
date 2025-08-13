


import dash
from dash import html, dcc
import dash_echarts
import requests
from config import API_URL, DASH_HOST, DASH_PORT

from urllib.parse import parse_qs

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Dropdown(
            id='period-selector',
            options=[
                {'label': '1 Day', 'value': '1d'},
                {'label': '1 Week', 'value': '5d'},
                {'label': '1 Month', 'value': '1mo'},
                {'label': '3 Months', 'value': '3mo'},
                {'label': '6 Months', 'value': '6mo'},
                {'label': '1 Year', 'value': '1y'},
                {'label': '2 Years', 'value': '2y'},
                {'label': '5 Years', 'value': '5y'},
                {'label': 'Max', 'value': 'max'}
            ],
            value='1y',
            style={'width': '150px', 'margin-bottom': '10px'}
        )
    ], style={'position': 'absolute', 'top': '10px', 'right': '10px', 'z-index': '100'}),
    dcc.Interval(id='interval', interval=60*1000, n_intervals=0),
    dash_echarts.DashECharts(
        id='stock-chart',
        style={'width': '100%', 'height': '600px'}
    )
])

@app.callback(
    dash.dependencies.Output('stock-chart', 'option'),
    [
        dash.dependencies.Input('interval', 'n_intervals'),
        dash.dependencies.Input('url', 'search'),
        dash.dependencies.Input('period-selector', 'value')
    ]
)
def update_chart(n, search, period):
    try:
        # Get symbol from URL parameters
        params = parse_qs(search[1:]) if search else {}
        symbol = params.get('symbol', ['AAPL'])[0]
        
        # Fetch data for requested symbol
        response = requests.get(f'{API_URL}/api/stocks/{symbol}?period={period}')
        data = response.json()
        stock_data = data['timeseries']
        
        # Prepare data for ECharts
        dates = [point['date'] for point in stock_data]
        prices = [point['price'] for point in stock_data]
        volumes = [point['volume'] for point in stock_data]
        
        option = {
            'title': {'text': f'{symbol} Stock Price History ({data["period"]})'},
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
        import traceback
        print(f"Error updating chart: {e}")
        print(traceback.format_exc())
        return {}

if __name__ == '__main__':
    app.run(host=DASH_HOST, port=DASH_PORT, debug=True)


