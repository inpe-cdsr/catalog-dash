# -*- coding: utf-8 -*-

from datetime import datetime as dt
from json import loads

from dash.dependencies import Input, Output
from dash.development.base_component import Component

from app import app
from modules.logging import logging

from apps.download.layout import *
from apps.download.service import __convert_dates_from_str_to_date, \
                                  __create_sub_df_based_on_parameters, \
                                  __get_geojson_data, color_prop, get_minmax_from_df
from apps.service import __get_date_picker_range_message, \
                         __get_figure_of_graph_bubble_map_number_of_scenes


minmax = get_minmax_from_df(df_d_email_scene_id_date)


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
def download__update_tables_by_parameters(start_date, end_date, limit):
    logging.info('download__update_tables_by_parameters()')

    logging.info('download__update_tables_by_parameters() - start_date: %s', start_date)
    logging.info('download__update_tables_by_parameters() - end_date: %s', end_date)
    logging.info('download__update_tables_by_parameters() - limit: %s', limit)

    # if limit is None, then the callback returns empty tables
    if limit is None:
        return [], []

    start_date, end_date = __convert_dates_from_str_to_date(start_date, end_date)

    sub_df_d_scene_id = __create_sub_df_based_on_parameters(
        df_d_scene_id_date, start_date, end_date, limit
    )

    sub_df_d_email = __create_sub_df_based_on_parameters(
        df_d_email_without_location, start_date, end_date, limit
    )

    return sub_df_d_scene_id.to_dict('records'), sub_df_d_email.to_dict('records')


@app.callback(
    Output('download--graph--bubble-map--number-of-downloaded-scenes-by-users', 'figure'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date'),
    Input('download--input--limit', 'value')])
def download__update_chart_by_parameters(start_date, end_date, limit):
    logging.info('download__update_chart_by_parameters()')

    logging.info('download__update_chart_by_parameters() - start_date: %s', start_date)
    logging.info('download__update_chart_by_parameters() - end_date: %s', end_date)
    logging.info('download__update_chart_by_parameters() - limit: %s', limit)

    # if limit is None, then the callback returns an empty chart
    if limit is None:
        return {"data": [], "layout": {}, "frames": []}

    start_date, end_date = __convert_dates_from_str_to_date(start_date, end_date)

    sub_df = __create_sub_df_based_on_parameters(
        df_d_email_scene_id_date, start_date, end_date, limit
    )

    figure = __get_figure_of_graph_bubble_map_number_of_scenes(
        sub_df,
        sort_by=['date'],
        title='Graph - Number of Downloaded Scenes by User in a specific location (long/lat)',
        color='email',
        # animation_frame='date',
        hover_data=['date'],
        plot_type='scatter_mapbox'
    )

    return figure


@app.callback(
    Output('download--map--number-of-downloaded-scenes-by-users', 'data'),
    [Input('download--date-picker-range', 'start_date'),
    Input('download--date-picker-range', 'end_date'),
    Input('download--input--limit', 'value')])
def download__update_map_by_parameters(start_date, end_date, limit):
    logging.info('download__update_map_by_parameters()')

    logging.info('download__update_map_by_parameters() - start_date: %s', start_date)
    logging.info('download__update_map_by_parameters() - end_date: %s', end_date)
    logging.info('download__update_map_by_parameters() - limit: %s', limit)

    # if limit is None, then the callback returns an empty map
    if limit is None:
        return Component.UNDEFINED

    start_date, end_date = __convert_dates_from_str_to_date(start_date, end_date)

    sub_df = __create_sub_df_based_on_parameters(
        df_d_email_scene_id_date, start_date, end_date, limit
    )

    # build the geojson object with a list of markers
    geojson = __get_geojson_data(sub_df)

    return geojson


@app.callback(
    [Output("download--map--number-of-downloaded-scenes-by-users", "hideout"),
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
