# -*- coding: utf-8 -*-

import plotly.express as px
from plotly.graph_objects import Figure, Bar

from apps.service import __get_logical_date_range
from modules.exception import CatalogDashException
from modules.logging import logging
from modules.utils import colors


##################################################
# layout services
##################################################

def copy_and_organize_df(df):
    # create a copy from the original df
    df_copy = df.copy()

    # extract year_month from my date
    df_copy['year_month'] = df_copy['date'].map(lambda date: date.strftime('%Y-%m'))

    return df_copy


##################################################
# callback services
##################################################

def get_figure_of_graph_bar_plot_number_of_scenes(df, xaxis_range=[], title=None, animation_frame=None,
                                                  is_scatter_geo=True, sort_ascending=True,
                                                  sort_by=['year_month', 'dataset']):
    logging.info('get_figure_of_graph_bar_plot_number_of_scenes()')

    figure_height = 800
    df_copy = df.copy()

    logging.info('get_figure_of_graph_bar_plot_number_of_scenes() - df_copy.head(): \n%s\n', df_copy.head())
    logging.info('get_figure_of_graph_bar_plot_number_of_scenes() - xaxis_range: %s\n', xaxis_range)

    logical_date_range = __get_logical_date_range(df_copy, xaxis_range)

    # I'm goint to build the `data` parameter of `Figure`
    data = []

    # I would like to build each `bar` based on each dataset
    for dataset in df_copy['dataset'].unique():
        sub_df = df_copy[(df_copy['dataset'] == dataset) & logical_date_range]

        hovertext = 'Number of Scenes: ' + sub_df['amount'].map(str) + '<br>' + \
                    'Period: ' + sub_df['year_month'].map(str) + '<br>' + \
                    'Dataset: ' + sub_df['dataset'].map(str)

        data.append(
            Bar(
                {
                    'x': sub_df['year_month'],
                    'y': sub_df['amount'],
                    'name': dataset,
                    'text': sub_df['amount'],  # text inside the bar
                    'textposition': 'auto',
                    'hovertext': hovertext,
                }
            )
        )

    fig = Figure(
        {
            'data': data,
            'layout': {
                'title': title,
                'xaxis': {'title': 'Period'},
                'yaxis': {'title': 'Number of scenes'},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )

    fig.update_layout(barmode='group', height=figure_height, xaxis_tickangle=-45)

    return fig
