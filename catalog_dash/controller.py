# -*- coding: utf-8 -*-

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from catalog_dash.model import DatabaseConnection
from catalog_dash.log import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


def create_app():
    app = Dash(__name__, external_stylesheets=external_stylesheets)
    db = DatabaseConnection()

    df = db.select_from_graph_amount_scenes_by_dataset_and_date()
    # df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

    df['formmated_date'] = pd.to_datetime(df['date'])

    print('\n df: \n', df.head())
    print('\n dtypes: \n', df.dtypes)
    print('\n dataset: ', df.dataset.unique())
    print('\n CBERS4A_MUX_L2_DN: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN'].head())
    print('\n date: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['date'].head())
    print('\n formmated_date: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['formmated_date'].head())
    print('\n amount: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['amount'].head())

    # title = 'catalog-dash'

    app.layout = html.Div([
        html.H1(children='catalog-dash'),
        dcc.Graph(
            id='graph-01',
            figure={
                'data': [
                    dict(
                        x=df[df['dataset'] == i]['formmated_date'],
                        y=df[df['dataset'] == i]['amount'],
                        text=i,
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df.dataset.unique()
                ],
                'layout': dict(
                    xaxis={'type': 'log', 'title': 'Date'},
                    yaxis={'title': 'Amount of scenes'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        ),
        dcc.Graph(
            id='graph-02',
            figure={
                'data': [dict(
                    x=df['date'],
                    y=df['amount'],
                    mode='lines+markers'
                )],
                'layout': {
                    # 'height': 225,
                    'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
                    'annotations': [{
                        'x': 0,
                        'y': 0.85,
                        # 'xanchor': 'left',
                        # 'yanchor': 'bottom',
                        'xref': 'paper',
                        'yref': 'paper',
                        'showarrow': False,
                        'align': 'left',
                        'bgcolor': 'rgba(255, 255, 255, 0.5)',
                        # 'text': title
                    }],
                    'yaxis': {'type': 'linear'},
                    # 'xaxis': {'showgrid': False}
                }
            }
        )
        # dcc.Graph(
        #     id='life-exp-vs-gdp',
        #     figure={
        #         'data': [
        #             dict(
        #                 x=df[df['continent'] == i]['gdp per capita'],
        #                 y=df[df['continent'] == i]['life expectancy'],
        #                 text=df[df['continent'] == i]['country'],
        #                 mode='markers',
        #                 opacity=0.7,
        #                 marker={
        #                     'size': 15,
        #                     'line': {'width': 0.5, 'color': 'white'}
        #                 },
        #                 name=i
        #             ) for i in df.continent.unique()
        #         ],
        #         'layout': dict(
        #             xaxis={'type': 'log', 'title': 'GDP Per Capita'},
        #             yaxis={'title': 'Life Expectancy'},
        #             margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        #             legend={'x': 0, 'y': 1},
        #             hovermode='closest'
        #         )
        #     }
        # )
    ])

    return app
