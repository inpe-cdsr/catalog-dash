# -*- coding: utf-8 -*-

from dash.dependencies import Input, Output
from datetime import datetime as dt
from re import split

from app import app
from modules.logging import logging

from apps.download.layout import *
from apps.service import __get_logical_date_range, __get_date_picker_range_message


@app.callback(
    Output('download--output-container-date-picker-range', 'children'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date')])
def download__update_output_container_date_picker_range(start_date, end_date):
    return __get_date_picker_range_message(start_date, end_date)


@app.callback(
    [Output('download--table--number-of-downloaded-scenes-by-scene_id-year_month', 'data'),
    Output('download--table--number-of-downloaded-scenes-by-user_id-scene_id-year_month', 'data')],
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date')])
def download__update_tables_by_date_picker_range_values(start_date, end_date):

    logging.info('download__update_tables()\n')

    logging.info('download__update_tables() - start_date: %s', start_date)
    logging.info('download__update_tables() - end_date: %s', end_date)

    # get just the date from [start|end]_dates
    xaxis_range = [start_date.split('T')[0], end_date.split('T')[0]]

    logging.info('download__update_tables() - xaxis_range: %s\n', xaxis_range)

    # create a sub dataframe based on start and end dates
    logical_date_range = __get_logical_date_range(df_d_scene_id_year_month, xaxis_range)
    sub_df_d_scene_id = df_d_scene_id_year_month[logical_date_range]

    # create a sub dataframe based on start and end dates
    logical_date_range = __get_logical_date_range(df_d_user_id_scene_id_year_month, xaxis_range)
    sub_df_d_user_id = df_d_user_id_scene_id_year_month[logical_date_range]

    # return the filtered records to each table
    return sub_df_d_scene_id.to_dict('records'), sub_df_d_user_id.to_dict('records')


# @app.callback(
#     Output('download--graph--bubble-map--number-of-downloaded-scenes-by-users', 'data'),
#     [Input('download--date-picker-range', 'start_date'),
#     Input('download--date-picker-range', 'end_date')])
# def download__update_charts_by_date_picker_range_values(start_date, end_date):

#     logging.info('download__update_charts()\n')

#     logging.info('download__update_charts() - start_date: %s', start_date)
#     logging.info('download__update_charts() - end_date: %s', end_date)

#     # get just the date from [start|end]_dates
#     xaxis_range = [start_date.split('T')[0], end_date.split('T')[0]]

#     logging.info('download__update_charts() - xaxis_range: %s\n', xaxis_range)
