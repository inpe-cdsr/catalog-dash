# -*- coding: utf-8 -*-

from dash.dependencies import Input, Output
from datetime import datetime as dt

from app import app
from modules.logging import logging

from apps.download.layout import *
from apps.service import __get_date_picker_range_message, \
                         __get_figure_of_graph_bubble_map_number_of_scenes


@app.callback(
    Output('download--output-container-date-picker-range', 'children'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date')])
def download__update_output_container_date_picker_range(start_date, end_date):
    return __get_date_picker_range_message(start_date, end_date)


@app.callback(
    [Output('download--table--number-of-downloaded-scenes-by-scene_id-date', 'data'),
    Output('download--table--number-of-downloaded-scenes-by-email-scene_id-date', 'data')],
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date'),
    Input('download--input--limit', 'value')])
def download__update_tables_by_date_picker_range_values(start_date, end_date, limit):
    logging.info('download__update_tables()')

    logging.info('download__update_tables() - start_date: %s', start_date)
    logging.info('download__update_tables() - end_date: %s', end_date)
    logging.info('download__update_tables() - limit: %s', limit)

    # if limit is None, then the callback returns empty tables
    if limit is None:
        return [], []

    # convert the [start|end]_date from str to date
    start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').date()
    end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').date()

    # create a sub dataframe based on start and end dates
    sub_df_d_scene_id = df_d_scene_id_date[
        ((df_d_scene_id_date['date'] >= start_date) & (df_d_scene_id_date['date'] <= end_date))
    ]

    sub_df_d_email = df_d_email_without_location[
        ((df_d_email_without_location['date'] >= start_date) & (df_d_email_without_location['date'] <= end_date))
    ]

    # reset the indexes to avoid the pandas warning related to SettingWithCopyWarning
    sub_df_d_scene_id.reset_index(drop=True, inplace=True)
    sub_df_d_email.reset_index(drop=True, inplace=True)

    # return the elements based on the limit, if it is possible
    if limit > 0 and limit < len(sub_df_d_scene_id.index):
        sub_df_d_scene_id = sub_df_d_scene_id.iloc[:limit]

    if limit > 0 and limit < len(sub_df_d_email.index):
        sub_df_d_email = sub_df_d_email.iloc[:limit]

    # return the filtered records to each table
    return sub_df_d_scene_id.to_dict('records'), sub_df_d_email.to_dict('records')


@app.callback(
    Output('download--graph--bubble-map--number-of-downloaded-scenes-by-users', 'figure'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date'),
    Input('download--input--limit', 'value')])
def download__update_charts_by_date_picker_range_values(start_date, end_date, limit):
    logging.info('download__update_charts()')

    logging.info('download__update_charts() - start_date: %s', start_date)
    logging.info('download__update_charts() - end_date: %s', end_date)
    logging.info('download__update_charts() - limit: %s', limit)

    # if limit is None, then the callback returns an empty graph
    if limit is None:
        return {"data": [], "layout": {}, "frames": []}

    # convert the [start|end]_date from str to date
    start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').date()
    end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').date()

    # get a sub set from the df according to the selected date range
    df_copy = df_d_email_scene_id_date[
        ((df_d_email_scene_id_date['date'] >= start_date) & (df_d_email_scene_id_date['date'] <= end_date))
    ]

    # reset the indexes to avoid the pandas warning related to SettingWithCopyWarning
    df_copy.reset_index(drop=True, inplace=True)

    # return the elements based on the limit, if it is possible
    if limit > 0 and limit < len(df_copy.index):
        df_copy = df_copy.iloc[:limit]

    df_copy['date'] = df_copy['date'].astype(str)

    figure = __get_figure_of_graph_bubble_map_number_of_scenes(
        df_copy,
        sort_by=['date'],
        title='Number of Downloaded Scenes by User in a specific location (long/lat)',
        color='email',
        # animation_frame='date',
        hover_data=['date'],
        plot_type='scatter_mapbox'
    )

    return figure
