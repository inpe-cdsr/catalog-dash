# -*- coding: utf-8 -*-

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.express as px

from catalog_dash.exception import CatalogDashException
from catalog_dash.logging import logging
from catalog_dash.utils import colors

# display a larger df on the console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


def get_figure_of_graph_bubble_map_amount_of_scenes(df, xaxis_range=[], title=None, animation_frame=None,
                                                    is_scatter_geo=True, sort_ascending=True,
                                                    sort_by=['year_month', 'dataset']):
    logging.info('get_figure_of_graph_bubble_map_amount_of_scenes()\n')

    figure_height = 800

    df_copy = df.copy()

    logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - df_copy.head(): \n%s\n', df_copy.head())
    logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - xaxis_range: %s\n', xaxis_range)

    logical_date_range = None

    # if there are values, then get a boolean df according to the selected date range
    if xaxis_range:
        # [:-3] - extract the string without the last 3 chars, in other words, I get just the year and month
        start_date = xaxis_range[0][:-3]
        end_date = xaxis_range[1][:-3]

        logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - start_date: %s', start_date)
        logging.info('get_figure_of_graph_bubble_map_amount_of_scenes() - end_date: %s\n', end_date)

        # extract a boolean df from the original one by the selected date range
        logical_date_range = ((df_copy['year_month'] >= start_date) & (df_copy['year_month'] <= end_date))
    else:
        raise CatalogDashException('Invalid `xaxis_range`, it is empty!')

    # get a sub set from the df according to the selected date range
    df_copy = df_copy[logical_date_range]

    # sort by date and dataset
    df_copy.sort_values(by=sort_by, ascending=sort_ascending, inplace=True)

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
