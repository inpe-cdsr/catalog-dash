# -*- coding: utf-8 -*-

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from catalog_dash.model import DatabaseConnection
from catalog_dash.log import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def get_text(df, dataset):
    sub_df = df[df['dataset'] == dataset]

    # logging.debug('get_text() - sub_df.head(): \n%s\n', sub_df.head())

    concat_df = 'Amount of Scenes: ' + sub_df['amount'].map(str) + '<br>' + \
                'Date: ' + sub_df['date'].map(str) + '<br>' + \
                'Dataset: ' + sub_df['dataset'].map(str)

    # logging.debug('get_text() - concat_df.head(): \n%s\n', concat_df.head())

    return concat_df


def create_app():
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
                    # 'opacity': 0.7,
                    # 'marker': {
                    #     'size': 15,
                    #     'line': {'width': 0.5, 'color': 'white'}
                    # },
                    'name': dataset
                } for dataset in df.dataset.unique()
            ],
            'layout': {
                'xaxis': {'title': 'Date'},
                'yaxis': {'title': 'Amount of scenes'},
                'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
                'legend': {'x': 0, 'y': 1},
                'hovermode': 'closest'
            }
        }
    )

    app.layout = html.Div([
        html.H1(children='catalog-dash'),
        graph_amount_of_scenes
    ])

    return app
