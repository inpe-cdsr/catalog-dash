# -*- coding: utf-8 -*-

from dash.dependencies import Input, Output
from datetime import datetime as dt
from re import split

from app import app
# from modules.exception import CatalogDashException
from modules.logging import logging

from apps.service import __get_date_picker_range_message
from apps.scene.layout import *
from apps.scene.service import get_figure_of_graph_bar_plot_number_of_scenes, \
                               get_figure_of_graph_bubble_map_number_of_scenes


@app.callback(
    Output('scene--output-container-date-picker-range', 'children'),
    [Input('scene--date-picker-range', 'start_date'),
    Input('scene--date-picker-range', 'end_date')])
def scene__update_output_container_date_picker_range(start_date, end_date):
    return __get_date_picker_range_message(start_date, end_date)


@app.callback(
    [Output('scene--graph--bar-plot--number-of-scenes', 'figure'),
    Output('scene--graph--bubble-map--number-of-scenes--with-animation-frame', 'figure')],
    [Input('scene--date-picker-range', 'start_date'),
    Input('scene--date-picker-range', 'end_date')])
def scene__update_graph_x_number_of_scenes_based_on_date_picker_range(start_date, end_date):
    logging.info('update_graph_number_of_scenes()\n')

    logging.info('update_graph_number_of_scenes() - start_date: %s', start_date)
    logging.info('update_graph_number_of_scenes() - end_date: %s', end_date)

    # convert the [start|end]_date from str to datetime
    start_date = dt.strptime(split('T| ', start_date)[0], '%Y-%m-%d')
    end_date = dt.strptime(split('T| ', end_date)[0], '%Y-%m-%d')

    # if start_date is None or start_date < min_start_date:
    #     raise CatalogDashException('The inserted start date is less than the minimum possible start date or it is None.')

    # if end_date is None or end_date > max_end_date:
    #     raise CatalogDashException('The inserted end date is greater than the maximum possible end date or it is None.')

    # convert the dates from datetime to str again in order to pass the xaxis range to build the figure
    xaxis_range = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

    logging.info('update_graph_number_of_scenes() - xaxis_range: %s\n', xaxis_range)

    figure_01 = get_figure_of_graph_bar_plot_number_of_scenes(df_sd_dataset_year_month,
                                                              xaxis_range=xaxis_range,
                                                              title='Number of Scenes by Dataset')

    figure_02 = get_figure_of_graph_bubble_map_number_of_scenes(df_sd_ds_ym_long_lat,
                                                                xaxis_range=xaxis_range,
                                                                title='Number of Scenes by Dataset in a specific location (long/lat)',
                                                                animation_frame='year_month')

    return figure_01, figure_02
