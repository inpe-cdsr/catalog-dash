# -*- coding: utf-8 -*-

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.express as px

from catalog_dash.exception import CatalogDashException
from catalog_dash.logging import logging
from catalog_dash.utils import colors, get_text

# display a larger df on the console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_figure_of_graph_time_series_amount_of_scenes(df, xaxis_range=[]):
    logging.info('get_figure_of_graph_amount_of_scenes()\n')

    logging.info('get_figure_of_graph_amount_of_scenes() - original df.head(): \n%s\n', df.head())

    logical_date_range = None

    # create the object `layout.xaxis`
    xaxis = {
        'title': 'Date',
        # 'range': ['2018-03-01', '2019-03-03']  # where the `range` key should be
    }

    # grouped_df = df.groupby(['dataset', 'date'], as_index=False).size().to_frame('amount').reset_index().sort_values(['date', 'dataset'])

    logging.info('get_figure_of_graph_amount_of_scenes() - grouped df.head(): \n%s\n', df.head())

    # if there are values, then do operations with the data, convert it and add it to the figure
    if xaxis_range:
        logging.info('get_figure_of_graph_amount_of_scenes() - inserted xaxis_range: %s\n', xaxis_range)

        # convert [start|end]_date from `str` to `datetime` in order to
        start_date = dt.strptime(xaxis_range[0], '%Y-%m-%d')
        end_date = dt.strptime(xaxis_range[1], '%Y-%m-%d')

        # extract the data from the original selected range
        logical_date_range = ((df['date'] >= start_date) & (df['date'] <= end_date))

        # substract and add months in order to make the graph look better
        start_date -= relativedelta(months=6)
        end_date += relativedelta(months=6)

        # convert the dates from `datetime` to `str` again in order to pass the xaxis range to build the figure
        xaxis_range = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        logging.info('get_figure_of_graph_amount_of_scenes() - converted xaxis_range: %s\n', xaxis_range)

        # add the `xaxis_range` to the figure
        xaxis['range'] = xaxis_range

    else:
        raise CatalogDashException('Invalid `xaxis_range`, it is empty!')

    return {
        'data': [
            {
                'x': df[(df['dataset'] == dataset) & (logical_date_range)]['date'],
                'y': df[(df['dataset'] == dataset) & (logical_date_range)]['amount'],
                'text': get_text(df[(df['dataset'] == dataset) & (logical_date_range)]),
                'mode': 'lines+markers',
                'opacity': 0.7,
                'marker': {'size': 7},
                'name': dataset
            } for dataset in df.dataset.unique()
        ],
        'layout': {
            'title': 'Time series',
            'xaxis': xaxis,
            'yaxis': {'title': 'Amount of scenes'},
            'margin': {'l': 40, 'b': 40, 't': 30, 'r': 10},
            'legend': {'x': 0, 'y': 1},
            'hovermode': 'closest',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }


def get_figure_of_graph_bubble_map_amount_of_scenes(df, xaxis_range=[], title=None, animation_frame=None,
                                                    is_scatter_geo=True, sort_ascending=True):
    logging.info('get_figure_of_graph_bubble_map_amount_of_scenes()\n')

    figure_height = 800

    df_copy = df.copy()

    # sort by date and dataset
    df_copy = df_copy.sort_values(by=['year_month', 'dataset'], ascending=sort_ascending)

    # logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - df_copy was sorted')
    # logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - df_copy.head(): \n%s\n', df_copy.head())
    # logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - df_copy.dtypes: \n%s\n', df_copy.dtypes)
    # logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - df_copy.shape: %s\n', df_copy.shape)

    # choose the map type based on the passed flag
    if is_scatter_geo:
        # create a figure using `px.scatter_geo`
        fig = px.scatter_geo(
            df_copy,
            title=title,
            lon='longitude',
            lat='latitude',
            color='dataset',
            size='amount',
            hover_data=['year_month'],
            animation_frame=animation_frame,
            projection='natural earth',
            height=figure_height
        )

        # update the flag
        fig.update_geos(showcountries=True)
    else:
        # create a figure using `px.scatter_mapbox`
        fig = px.scatter_mapbox(
            df_copy,
            title=title,
            lon='longitude',
            lat='latitude',
            color='dataset',
            size='amount',
            hover_data=['year_month'],
            animation_frame=animation_frame,
            zoom=2,
            height=figure_height
        )

        # add as base map the OSM
        fig.update_layout(
            mapbox_style='open-street-map',
            margin={'t': 40, 'r': 5, 'b': 5, 'l': 5}
        )

    return fig
