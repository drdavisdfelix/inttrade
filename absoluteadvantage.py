import dash
import numpy as np
import plotly.graph_objs as go
import os
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server  # gunicorn to detect the app for Heroku deployment

# Function to generate y values for the indifference curves
def g(t, c):
    return c / (t + 1)**2

app.layout = html.Div([
    html.Div([
        html.Label('Country 1 at Autarky:'),
        dcc.Input(id='country1-autarky-a', type='number', placeholder='A value'),
        dcc.Input(id='country1-autarky-b', type='number', placeholder='B value')
    ]),
    html.Div([
        html.Label('Country 1 at Trade:'),
        dcc.Input(id='country1-trade-a', type='number', placeholder='A value'),
        dcc.Input(id='country1-trade-b', type='number', placeholder='B value')
    ]),
    html.Div([
        html.Label('Country 2 at Autarky:'),
        dcc.Input(id='country2-autarky-a', type='number', placeholder='A value'),
        dcc.Input(id='country2-autarky-b', type='number', placeholder='B value')
    ]),
    html.Div([
        html.Label('Country 2 at Trade:'),
        dcc.Input(id='country2-trade-a', type='number', placeholder='A value'),
        dcc.Input(id='country2-trade-b', type='number', placeholder='B value')
    ]),
    html.Div([
        dcc.Input(id='x-axis-label', type='text', placeholder='X-Axis Label'),
        dcc.Input(id='y-axis-label', type='text', placeholder='Y-Axis Label'),
        dcc.Input(id='chart-title', type='text', placeholder='Chart Title')
    ]),
    dcc.Graph(id='indifference-curve-plot')
])
])

@app.callback(
    Output('indifference-curve-plot', 'figure'),
    [
        Input('country1-autarky-a', 'value'), Input('country1-autarky-b', 'value'),
        Input('country1-trade-a', 'value'), Input('country1-trade-b', 'value'),
        Input('country2-autarky-a', 'value'), Input('country2-autarky-b', 'value'),
        Input('country2-trade-a', 'value'), Input('country2-trade-b', 'value'),
        Input('x-axis-label', 'value'), Input('y-axis-label', 'value'),
        Input('chart-title', 'value')
    ]
)
def update_graph(
    c1a_a, c1a_b, c1t_a, c1t_b,
    c2a_a, c2a_b, c2t_a, c2t_b,
    x_axis_label, y_axis_label, chart_title
):
    a = 0.5
    points = [(c1a_a, c1a_b), (c1t_a, c1t_b), (c2a_a, c2a_b), (c2t_a, c2t_b)]
    fig = go.Figure()

    # Function to generate y values for the indifference curves
    def generate_y_values(t_values, c_values):
        return [g(t, c) for t, c in zip(t_values, c_values)]

    for idx, point in enumerate(points):
        if point[0] and point[1]:  # Checking to see if the values are not None
            t_values = np.linspace(1, int(point[0]*2), 400)
            y_values = generate_y_values(t_values, [point[0]] * len(t_values))
            fig.add_trace(go.Scatter(x=t_values, y=y_values, mode='lines', name=f'Country {idx//2 + 1} - {"Autarky" if idx % 2 == 0 else "Trade"}'))

    fig.update_layout(title=chart_title, xaxis_title=x_axis_label, yaxis_title=y_axis_label)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 8051)))

