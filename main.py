# -*- coding: utf-8 -*-

from datetime import datetime as dt
from re import split

from dash import Dash
from dash_core_components import Graph, DatePickerRange
from dash.dependencies import Output, Input
from dash_html_components import Div, H1, H3

from catalog_dash.components import get_figure_of_graph_time_series_amount_of_scenes, \
                                    get_figure_of_graph_bubble_map_amount_of_scenes
from catalog_dash.environment import DEBUG_MODE
from catalog_dash.exception import CatalogDashException
from catalog_dash.logging import logging
from catalog_dash.model import DatabaseConnection
from catalog_dash.utils import colors, external_stylesheets, get_formatted_date_as_string


app = Dash(__name__, external_stylesheets=external_stylesheets)
db = DatabaseConnection()

df = db.select_from_graph_amount_scenes_by_dataset_and_date()


logging.info('main.py - df.head(): \n%s\n', df.head())
logging.info('main.py - df.shape: %s\n', df.shape)
logging.info('main.py - df.dtypes: \n%s\n', df.dtypes)

# get the min start date and the max end date to the graph
min_start_date = df['date'].min()  # min_start_date: 2016-05-01 00:00:00
max_end_date = df['date'].max()  # max_end_date: 2020-03-03 00:00:00

logging.info('main.py - min_start_date: %s', min_start_date)
logging.info('main.py - max_end_date: %s', max_end_date)


app.layout = Div(style={'backgroundColor': colors['background']}, children=[
    # title
    H1(
        children='catalog-dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # date picker range
    Div([
        # Source: https://dash.plotly.com/dash-core-components/datepickerrange
        DatePickerRange(
            id='date-picker-range',
            display_format='DD/MM/YYYY',
            min_date_allowed=min_start_date,
            max_date_allowed=max_end_date,
            start_date=min_start_date,
            end_date=max_end_date
        )
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    H3(
        id='output-container-date-picker-range',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # graph-time-series-amount-of-scenes
    Graph(id='graph-time-series-amount-of-scenes'),

    # graph-bubble-map-amount-of-scenes
    # Graph(id='graph-bubble-map-amount-of-scenes')
])


@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')])
def update_output_container_date_picker_range(start_date, end_date):
    # Source: https://dash.plotly.com/dash-core-components/datepickerrange

    string_prefix = ''

    if start_date is not None:
        string_prefix += 'Start Date: ' + get_formatted_date_as_string(start_date) + ' | '

    if end_date is not None:
        string_prefix += 'End Date: ' + get_formatted_date_as_string(end_date)

    if string_prefix == '':
        return 'Select a date to see it displayed here'

    return string_prefix


@app.callback(
    Output('graph-time-series-amount-of-scenes', 'figure'),
    # [Output('graph-time-series-amount-of-scenes', 'figure'),
    # Output('graph-bubble-map-amount-of-scenes', 'figure')],
    [Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')])
def update_graph_x_amount_of_scenes_based_on_date_picker_range(start_date, end_date):
    logging.info('update_graph_amount_of_scenes()\n')

    logging.info('update_graph_amount_of_scenes() - start_date: %s', start_date)
    logging.info('update_graph_amount_of_scenes() - end_date: %s', end_date)

    # convert the [start|end]_date from str to datetime
    start_date = dt.strptime(split('T| ', start_date)[0], '%Y-%m-%d')
    end_date = dt.strptime(split('T| ', end_date)[0], '%Y-%m-%d')

    if start_date is None or start_date < min_start_date:
        raise CatalogDashException('The inserted start date is less than the minimum possible start date or it is None.')

    if end_date is None or end_date > max_end_date:
        raise CatalogDashException('The inserted end date is greater than the maximum possible end date or it is None.')

    # convert the dates from datetime to str again in order to pass the xaxis range to build the figure
    xaxis_range = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

    logging.info('update_graph_amount_of_scenes() - xaxis_range: %s\n', xaxis_range)

    return get_figure_of_graph_time_series_amount_of_scenes(df, xaxis_range=xaxis_range)
    # return get_figure_of_graph_time_series_amount_of_scenes(df, xaxis_range=xaxis_range), \
    #        get_figure_of_graph_bubble_map_amount_of_scenes(df, xaxis_range=xaxis_range)


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE)
