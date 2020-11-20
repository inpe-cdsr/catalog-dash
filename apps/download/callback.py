# -*- coding: utf-8 -*-

from datetime import datetime as dt
from json import loads

from dash.dependencies import Input, Output
from dash.development.base_component import Component
from dash_leaflet.express import dicts_to_geojson

from app import app
from modules.logging import logging

from apps.download.layout import *
from apps.download.service import __convert_dates_from_str_to_date, \
                                  __create_sub_df_based_on_parameters, \
                                  __get_geojson_data, color_prop, get_minmax_from_df
from apps.service import __get_date_picker_range_message, \
                         __get_figure_of_graph_bubble_map_number_of_scenes


minmax = get_minmax_from_df(df_d_base)


@app.callback(
    Output('download--output-container-date-picker-range', 'children'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date')])
def download__update_output_container_date_picker_range(start_date, end_date):
    return __get_date_picker_range_message(start_date, end_date)


@app.callback(
    [Output('download--table--number-of-downloaded-scenes-by-date', 'data'),
    Output('download--table--number-of-downloaded-scenes-by-user-and-date', 'data')],
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date'),
    Input('download--input--limit', 'value')])
def download__update_tables_by_parameters(start_date, end_date, limit):
    logging.info('download__update_tables_by_parameters()')

    logging.info('download__update_tables_by_parameters() - start_date: %s', start_date)
    logging.info('download__update_tables_by_parameters() - end_date: %s', end_date)
    logging.info('download__update_tables_by_parameters() - limit: %s', limit)

    start_date, end_date = __convert_dates_from_str_to_date(start_date, end_date)

    # if start date is greater than end date or limit is None, then the callback returns an empty object
    if start_date > end_date or limit is None:
        return [], []

    # filter base dataframe based on start date, end date and limit
    sub_df_d_base = __create_sub_df_based_on_parameters(
        df_d_base, start_date, end_date, limit
    )

    # filter the previous dataframe to get the number of downloaded scenes by user and date
    sub_df_ndsb_user_date = sub_df_d_base.groupby(['user_id', 'name', 'date'])['number'].sum().to_frame('number').reset_index()
    sub_df_ndsb_user_date = sub_df_ndsb_user_date.sort_values(['number'], ascending=False)

    # filter the previous dataframe to get the number of downloaded scenes by date only
    sub_df_ndsb_date = sub_df_ndsb_user_date.groupby(['date'])['number'].sum().to_frame('number').reset_index()
    sub_df_ndsb_date = sub_df_ndsb_date.sort_values(['number'], ascending=False)

    # I get the last column and I add it to the beginning
    columns_df_ndsb_date = sub_df_ndsb_date.columns.tolist()
    columns_df_ndsb_date = columns_df_ndsb_date[-1:] + columns_df_ndsb_date[:-1]
    sub_df_ndsb_date = sub_df_ndsb_date[columns_df_ndsb_date]

    return sub_df_ndsb_date.to_dict('records'), \
           sub_df_ndsb_user_date.to_dict('records')


@app.callback(
    Output('download--map--number-of-downloaded-scenes-by-location', 'data'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date'),
    Input('download--input--limit', 'value')])
def download__update_map_by_parameters(start_date, end_date, limit):
    logging.info('download__update_map_by_parameters()')

    logging.info('download__update_map_by_parameters() - start_date: %s', start_date)
    logging.info('download__update_map_by_parameters() - end_date: %s', end_date)
    logging.info('download__update_map_by_parameters() - limit: %s', limit)

    start_date, end_date = __convert_dates_from_str_to_date(start_date, end_date)

    # if start date is greater than end date or limit is None, then the callback returns an empty object
    if start_date > end_date or limit is None:
        return dicts_to_geojson([])

    sub_df = __create_sub_df_based_on_parameters(
        df_d_base, start_date, end_date, limit
    )

    # build the geojson object with a list of markers
    return __get_geojson_data(sub_df)


@app.callback(
    [Output("download--map--number-of-downloaded-scenes-by-location", "hideout"),
    Output("download--map--colorbar", "colorscale"),
    Output("download--map--colorbar", "min"),
    Output("download--map--colorbar", "max")],
    [Input("download--map--dropdown--color-scale", "value")])
def download__update_map_colorbar(csc):
    csc = loads(csc)
    hideout = {
        'colorscale': csc,
        'color_prop': color_prop,
        **minmax
    }
    return hideout, csc, minmax["min"], minmax["max"]
