
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
from scipy.stats import poisson, geom
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = [('poisson distribution', 1), ('geometric distribution', 2), ('normal distribution',3)]

app.layout = html.Div(
    children=[
        html.Div(
            style={'backgroundColor': '#1b1f34', 'height': '200%', 'padding-bottom': '30px', 'padding-top': '20px'},
            children=[
                html.H1(children="Probability distributions", style={'textAlign': 'center', 'color': '#c6c6c6'}),
                html.P(
                    children="Choose one of tree common probability distribution and change its parameter/parameters",
                    style={'textAlign': 'center', 'color': '#c6c6c6'}
                )]),
        html.Br(),
        html.Div(
            style={'width': '50%', 'margin': 'auto', 'margin-top': '40px', 'margin-bottom': '40px'},
            children=[
                # using plotly
                dcc.Dropdown(
                    id='distribution',
                    options=[{'label': i, 'value': j} for i, j in available_indicators],
                    value='distribution',
                    placeholder="pick a given distribution",

                ),
                html.Br(),
                        html.Div([
                        html.P('expected value', style={'margin-left':'8%'}),
                        dcc.Input(id='my-input',
                                  type='number',
                                  placeholder="enter expected value (average)",

                                  value=2.5
                                  ),
                                ], style={'display':'none'},id='my-input-display' ),
                        html.Div([
                        html.P('expected value', style={'margin-left':'8%'}),
                        dcc.Input(id='my-input-2',
                                  type='number',
                                  placeholder="enter expected value (average)",
                                  value=0.16
                                  ),
                                ], style={'display':'none'}, id='my-input-2-display'),


                        html.Div([
                            html.P('mean', style={'textAlign':'center'}),
                            dcc.Slider(id="mean", min=-3, max=3, value=0,
                                marks={-3: '-3', 3: '3'}),

                            html.P('std', style={'textAlign':'center'}),
                            dcc.Slider(id="std", min=1, max=3, value=1,
                                marks={1: '1', 3: '3'}),
                        ], style={'width': '50%', 'margin': 'auto', 'display':'none'}, id="display-slider")
            ]),

        dcc.Graph(id='indicator-graphic'),

    ]
)




# it is actually a decorator of function update graph
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('distribution', 'value'),
     Input('my-input', 'value'),
     Input('my-input-2', 'value'),
     Input("mean", "value"),
     Input("std", "value")])
def update_graph(value, mu, k, mean, sigma):
    if mu is None or k is None or mean is None or sigma is None:
        raise PreventUpdate
    else:
        if value == 1:
            possible_outcomes = []
            for i in range(10):
                possible_outcomes.append(poisson.pmf(mu=mu, k=i))
            x_axis = [i for i in range(0, 10)]
            fig = px.bar(x=x_axis, y=possible_outcomes)
            return fig

        elif value == 2:
            possible_outcomes = []
            for i in range(10):
                possible_outcomes.append(geom.pmf(p=k, k=i))
            x = [i for i in range(0, 10)]
            fig = px.bar(x=x, y=possible_outcomes)
            return fig
        else:
            norm = np.random.normal(mean, sigma,1000)
            fig = px.histogram(norm)
            return fig




# displaying or hiding elements

@app.callback(
    Output('my-input-display', component_property='style'),
    [Input('distribution', 'value')]
)
def update_style(value):
    """
       displaying parameter for poisson distribution
    """
    if value == 1:
        return  {'width': '50%', 'margin': 'auto', 'display':'inline-block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output('my-input-2-display', component_property='style'),
    [Input('distribution', 'value')]
)
def update_style(value):
    """
       displaying parameter for poisson distribution
    """
    if value== 2:
        return {'width': '50%', 'margin': 'auto', 'display':'inline-block'}
    else:
        return {'display': 'none'}



@app.callback(
    Output('display-slider', component_property='style'),
    [Input('distribution', 'value')]
)
def update_style(value):
    """
       displaying parameter for poisson distribution
    """
    if value == 3:
        return {'display': 'inline', 'width':'50%'}
    else:
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
