# -*- coding: utf-8 -*-

import pandas as pd
from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from catalog_dash.environment import DEBUG_MODE
from catalog_dash.log import logging
from catalog_dash.model import DatabaseConnection
from catalog_dash.util import external_stylesheets, colors, get_text


app = Dash(__name__, external_stylesheets=external_stylesheets)
db = DatabaseConnection()

df = db.select_from_graph_amount_scenes_by_dataset_and_date()

# print('\n df: \n', df.head())
# print('\n dtypes: \n', df.dtypes)
# print('\n dataset: ', df.dataset.unique())
# print('\n CBERS4A_MUX_L2_DN: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN'].head())
# print('\n date: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['date'].head())
# print('\n amount: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['amount'].head())

graph_amount_of_scenes = dcc.Graph(
    id='graph-01',
    figure={
        'data': [
            {
                'x': df[df['dataset'] == dataset]['date'],
                'y': df[df['dataset'] == dataset]['amount'],
                # text=df[df['continent'] == i]['country'],
                'text': get_text(df, dataset),
                'mode': 'lines+markers',
                'opacity': 0.7,
                'marker': {
                    'size': 7,
                    # 'line': {'width': 0.5, 'color': 'white'}
                },
                'name': dataset
            } for dataset in df.dataset.unique()
        ],
        'layout': {
            'xaxis': {'title': 'Date'},
            'yaxis': {'title': 'Amount of scenes'},
            'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
            'legend': {'x': 0, 'y': 1},
            'hovermode': 'closest',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }
)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='catalog-dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    graph_amount_of_scenes
])


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE)
