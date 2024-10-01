import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div(children=[
    html.H1(children='Gráfico de Doble Barra'),

    # Gráfico
    dcc.Graph(id='double-bar-graph'),

    # Intervalo de tiempo para actualizar (opcional)
    dcc.Interval(
        id='interval_time',
        interval=1 * 1000,  # Actualizar cada segundo
        n_intervals=0
    )
])

# Callback para generar el gráfico
@app.callback(
    Output('double-bar-graph', 'figure'),
    Input('interval_time', 'n_intervals')  # Esto es opcional para actualización
)
def update_graph(n_intervals):

    # Datos para el gráfico
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May']
    cds = [10, 12, 15, 18, 20]
    libros = [15, 18, 20, 25, 30]

    # Crear gráfico de barras agrupadas
    fig = go.Figure(data=[
        go.Bar(name='CD de música', x=meses, y=cds, marker_color='blue'),
        go.Bar(name='Libros', x=meses, y=libros, marker_color='red')
    ])

    # Cambiar el layout del gráfico
    fig.update_layout(
        title='Crecimiento de la colección de Lisa',
        xaxis_title='Meses',
        yaxis_title='Número de artículos',
        barmode='group'  # Esto asegura que las barras estén agrupadas por categoría
    )

    return fig

# Ejecutar la aplicación en el servidor local
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
