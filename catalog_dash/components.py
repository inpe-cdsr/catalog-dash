# -*- coding: utf-8 -*-

from dash_core_components import Graph

from catalog_dash.utils import colors, get_text


def get_graph_amount_of_scenes(df):
    return Graph(
        id='graph_amount_of_scenes',
        figure={
            'data': [
                {
                    'x': df[df['dataset'] == dataset]['date'],
                    'y': df[df['dataset'] == dataset]['amount'],
                    # text=df[df['continent'] == i]['country'],
                    'text': get_text(df, dataset),
                    'mode': 'lines+markers',
                    'opacity': 0.7,
                    'marker': {'size': 7},
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