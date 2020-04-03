# -*- coding: utf-8 -*-

from catalog_dash.utils import colors, get_text


def get_figure_of_graph_amount_of_scenes(df, xaxis_range=[]):
    xaxis = {
        'title': 'Date',
        # 'range': ['2018-03-01', '2019-03-03']
    }

    # if there are values, then add it to the figure
    if xaxis_range:
        xaxis['range'] = xaxis_range

    return {
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
            'xaxis': xaxis,
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