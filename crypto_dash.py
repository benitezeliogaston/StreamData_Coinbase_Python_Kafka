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

    #cryptocurrency counting table
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

    #Total capital transferred 
    dcc.Graph(id="capital"),


    #Counter sell/buy for each cryptocurrency
    dcc.Graph(id='counter_sell_buy'),

    #time interval
    dcc.Interval(
        id='interval_time',
        interval=5 * 1000,  #update dash for each 5 seconds
        n_intervals=0
    )
])


#Execute callback for each 5 seconds
@app.callback(
    [Output('crypto_table', 'data'), #Cryptocurrency table
     Output('capital', 'figure'), # Total capital transferred 
     Output('counter_sell_buy','figure'),],  # Count buy/sell 
    [Input('interval_time', 'n_intervals')]
)
def update_data(n_intervals):
    
    instancia.update_vars()


    # Crear los datos para la tabla
    table_data = [
        {'cryptocurrency': 'BTC', 'amount_transferred': instancia.btc_size},
        {'cryptocurrency': 'ETH', 'amount_transferred': instancia.eth_size},
        {'cryptocurrency': 'SOL', 'amount_transferred': instancia.sol_size}
    ]

    # Crear el gráfico de capital transferido
    figure_capital = {
        'data': [
            {
                'x': ['BTC', 'ETH', 'SOL'],
                'y': [instancia.btc_capital, instancia.eth_capital, instancia.sol_capital],
                'type': 'bar'
            }
        ],
        'layout': {
            'title': 'Capital Transferred in Cryptocurrencies'
        }
    }



    #Create counter sell/buy
    fig = go.Figure(data=[

        #Buy Bar
        go.Bar(
            name='Buy',
            x=['BTC','ETH','SOL'],
            y= [instancia.btc_buy,instancia.eth_buy,instancia.sol_buy],
            marker_color='blue'),

        #Sell Bar
        go.Bar(
            name='Sell',
            x=['BTC','ETH','SOL'],
            y=[instancia.btc_sell,instancia.eth_sell,instancia.sol_sell], 
            marker_color='red')
    ])

    #Update details
    fig.update_layout(
        title='Buy/Sell counter',

        xaxis_title='Counters',
        yaxis_title='Count buy/sell',

        barmode='group'  # Group bars
    )

    return table_data, figure_capital , fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
