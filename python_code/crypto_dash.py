import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import dash_table
from crypto_consumer import CryptoConsumer
import plotly.graph_objects as go

# === VAR TO DASH

# Create instance
instancia = CryptoConsumer()

# Create dash app
app = dash.Dash(__name__)

# LAYOUT APP
app.layout = html.Div(children=[
    html.H1(children='Buy/Sell Information from Coinbase'),

    html.P(children="This is one example of a real-time data stream. The idea is to get data from Coinbase and use it to create analytics information."),

    #Cryptocurrency counting table
    dash_table.DataTable(
        id='crypto_table',
        columns=[
            {'name': 'Cryptocurrency', 'id': 'cryptocurrency'},
            {'name': 'Amount Transferred', 'id': 'amount_transferred'}
        ],
        data=[],  #will be filled with each update
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    # Total capital transferred 
    dcc.Graph(id="capital"),

    # Three separate graphs for buy/sell counter
    html.Div([
        html.Div(dcc.Graph(id='counter_sell_buy_btc'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='counter_sell_buy_eth'), style={'width': '33%', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id='counter_sell_buy_sol'), style={'width': '33%', 'display': 'inline-block'}),
    ], style={'display': 'flex'}),

    # Time interval for updates
    dcc.Interval(
        id='interval_time',
        interval=5 * 1000,  #update every 5 seconds
        n_intervals=0
    )
])

# Execute callback for each 5 seconds
@app.callback(
    [Output('crypto_table', 'data'),  # Cryptocurrency table
     Output('capital', 'figure'),  # Total capital transferred 
     Output('counter_sell_buy_btc', 'figure'),  # BTC buy/sell counter
     Output('counter_sell_buy_eth', 'figure'),  # ETH buy/sell counter
     Output('counter_sell_buy_sol', 'figure')],  # SOL buy/sell counter
    [Input('interval_time', 'n_intervals')]
)
def update_data(n_intervals):
    
    instancia.update_vars()

    # Create data for table
    table_data = [
        {'cryptocurrency': 'BTC', 'amount_transferred': instancia.btc_size},
        {'cryptocurrency': 'ETH', 'amount_transferred': instancia.eth_size},
        {'cryptocurrency': 'SOL', 'amount_transferred': instancia.sol_size}
    ]

    # Create total capital transferred
    figure_capital = {
        'data': [
            {
                'x': ['BTC', 'ETH', 'SOL'],
                'y': [instancia.btc_capital, instancia.eth_capital, instancia.sol_capital],
                'type': 'bar',
                'marker': {'color': ['#FFD700', '#3C3CFF', '#FFA500']}  # Colors for BTC, ETH, SOL
            }
        ],
        'layout': {
            'title': 'Capital Transferred in Cryptocurrencies'
        }
    }

    # Create BTC buy/sell graph
    fig_btc = go.Figure(data=[
        go.Bar(name='Buy', x=['BTC'], y=[instancia.btc_buy], marker_color='green'),
        go.Bar(name='Sell', x=['BTC'], y=[instancia.btc_sell], marker_color='red')
    ])
    fig_btc.update_layout(title='BTC Buy/Sell', xaxis_title='Buy/Sell', yaxis_title='Count')

    # Create ETH buy/sell graph
    fig_eth = go.Figure(data=[
        go.Bar(name='Buy', x=['ETH'], y=[instancia.eth_buy], marker_color='green'),
        go.Bar(name='Sell', x=['ETH'], y=[instancia.eth_sell], marker_color='red')
    ])
    fig_eth.update_layout(title='ETH Buy/Sell', xaxis_title='Buy/Sell', yaxis_title='Count')

    # Create SOL buy/sell graph
    fig_sol = go.Figure(data=[
        go.Bar(name='Buy', x=['SOL'], y=[instancia.sol_buy], marker_color='green'),
        go.Bar(name='Sell', x=['SOL'], y=[instancia.sol_sell], marker_color='red')
    ])
    fig_sol.update_layout(title='SOL Buy/Sell', xaxis_title='Buy/Sell', yaxis_title='Count')

    return table_data, figure_capital, fig_btc, fig_eth, fig_sol


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
