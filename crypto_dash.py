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

    # Tabla para mostrar la cantidad de criptomonedas transferidas
    dash_table.DataTable(
        id='crypto_table',
        columns=[
            {'name': 'Cryptocurrency', 'id': 'cryptocurrency'},
            {'name': 'Amount Transferred', 'id': 'amount_transferred'}
        ],
        data=[],  # Inicialmente vacía, se llenará con cada actualización
        style_cell={'textAlign': 'left'},
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        },
    ),

    # Gráfico de capital transferido
    dcc.Graph(id="capital"),


    #Counter sell/buy
    dcc.Graph(id='counter_sell_buy'),


    #Grafico de volumen comprador y vendedor

    # Intervalo de tiempo
    dcc.Interval(
        id='interval_time',
        interval=5 * 1000,  # actualizar cada segundo
        n_intervals=0
    )
])


# Callback que se ejecuta en cada intervalo
@app.callback(
    [Output('crypto_table', 'data'), # Tabla de criptomonedas transferidas
     Output('capital', 'figure'),
     Output('counter_sell_buy','figure'),],  # COntador
    [Input('interval_time', 'n_intervals')]  # Input: Cada segundo
)
def update_data(n_intervals):
    print(".")
    
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
        go.Bar(
            name='Buy',
            x=['BTC','ETH','SOL'],
            y= [instancia.btc_buy,instancia.eth_buy,instancia.sol_buy],
            marker_color='blue'),

        go.Bar(
            name='Sell',
            x=['BTC','ETH','SOL'],
            y=[instancia.btc_sell,instancia.eth_sell,instancia.sol_sell], 
            marker_color='red')
    ])
    print(instancia.eth_buy)
    print(instancia.btc_sell)

    # Cambiar el layout del gráfico
    fig.update_layout(
        title='Compra venta de criptos',

        xaxis_title='Counters',
        yaxis_title='Count buy/sell',

        barmode='group'  # Esto asegura que las barras estén agrupadas por categoría
    )

    return table_data, figure_capital , fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
