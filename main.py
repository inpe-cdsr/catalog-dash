# -*- coding: utf-8 -*-

from datetime import datetime as dt
from re import split
from pandas import read_csv, to_datetime

from dash import Dash
from dash_core_components import Graph, DatePickerRange
from dash.dependencies import Output, Input
from dash_html_components import Div, H1, H3, H4
from dash_table import DataTable
from flask import Flask, redirect

from catalog_dash.components import get_figure_of_graph_bubble_map_amount_of_scenes
from catalog_dash.environment import IS_TO_USE_DATA_FROM_DB, DEBUG_MODE, SERVER_HOST, SERVER_PORT
from catalog_dash.exception import CatalogDashException
from catalog_dash.logging import logging
from catalog_dash.model import DatabaseConnection
from catalog_dash.utils import colors, external_stylesheets, get_formatted_date_as_string, extra_logging


logging.info('main.py - IS_TO_USE_DATA_FROM_DB: %s', IS_TO_USE_DATA_FROM_DB)
logging.info('main.py - DEBUG_MODE: %s', DEBUG_MODE)
logging.info('main.py - SERVER_HOST: %s', SERVER_HOST)
logging.info('main.py - SERVER_PORT: %s\n', SERVER_PORT)


# flask server
server = Flask(__name__)

@server.route('/')
def index():
    return redirect('/catalog-dash/')


# dash application
app = Dash(__name__, server=server, external_stylesheets=external_stylesheets, url_base_pathname='/catalog-dash/')


if IS_TO_USE_DATA_FROM_DB:
    # database connection
    db = DatabaseConnection()

    df_scene_dataset = db.select_from_scene_dataset()
    # df_scene_dataset.to_csv('data/scene_dataset.csv', index=False)

    df_amount_of_scenes = db.select_from_dash_amount_scenes_by_dataset_year_month_lon_lat()
    # df_amount_of_scenes.to_csv('data/amount_of_scenes.csv', index=False)
else:
    # get the data from a CSV file
    df_scene_dataset = read_csv('data/scene_dataset.csv')
    df_scene_dataset['date'] = to_datetime(df_scene_dataset['date'])

    df_amount_of_scenes = read_csv('data/amount_of_scenes.csv')


logging.info('main.py - df_scene_dataset.head(): \n%s\n', df_scene_dataset.head())
logging.info('main.py - df_scene_dataset.shape: %s\n', df_scene_dataset.shape)
logging.info('main.py - df_scene_dataset.dtypes: \n%s\n', df_scene_dataset.dtypes)
logging.info('main.py - type(df_scene_dataset): %s\n', type(df_scene_dataset))

extra_logging(df_scene_dataset)

logging.info('main.py - df_amount_of_scenes.head(): \n%s\n', df_amount_of_scenes.head())
logging.info('main.py - df_amount_of_scenes.shape: %s\n', df_amount_of_scenes.shape)
logging.info('main.py - df_amount_of_scenes.dtypes: \n%s\n', df_amount_of_scenes.dtypes)
logging.info('main.py - type(df_amount_of_scenes): %s\n', type(df_amount_of_scenes))


# get the values
amount_of_datasets = len(df_scene_dataset.dataset.unique())
min_start_date = df_scene_dataset['date'].min()  # min_start_date: 2016-05-01 00:00:00
max_end_date = df_scene_dataset['date'].max()  # max_end_date: 2020-03-03 00:00:00

logging.info('main.py - amount_of_datasets: %s', amount_of_datasets)
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

    # table--amount-of-scenes
    Div([
        DataTable(
            id='table--amount-of-scenes',
            columns=[{"name": i, "id": i} for i in df_amount_of_scenes.columns],
            data=df_amount_of_scenes.to_dict('records'),
            style_as_list_view=True,
            fixed_rows={ 'headers': True, 'data': 0 },
            style_table={
                'maxHeight': '300px',
                'maxWidth': '1000px',
                'overflowY': 'scroll'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(130, 130, 130)'
                }
            ],
            style_filter={
                'backgroundColor': 'white'
            },
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'year_month'},
                    'textAlign': 'center'
                }
            ],
            style_cell={
                'textAlign': 'left',
                'minWidth': '100px',
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            sort_action='native',
            sort_mode='multi',
            filter_action='native',
            page_size=50,
        ),
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    # amount of datasets
    H4(
        children='Amount of Datasets: {}'.format(amount_of_datasets),
        style={
            'textAlign': 'left',
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

    # graph--time-series--amount-of-scenes
    # Graph(id='graph--time-series--amount-of-scenes'),

    # graph--bubble-map--amount-of-scenes-by-dataset
    Graph(id='graph--bubble-map--amount-of-scenes-by-dataset')
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
    Output('graph--bubble-map--amount-of-scenes-by-dataset', 'figure'),
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

    # figure_01 = get_figure_of_graph_time_series_amount_of_scenes(df_amount_of_scenes, xaxis_range=xaxis_range)

    figure_02 = get_figure_of_graph_bubble_map_amount_of_scenes(df_amount_of_scenes,
                                                                xaxis_range=xaxis_range,
                                                                title='Amount of Scenes by Dataset in a specific location (long/lat)',
                                                                animation_frame='year_month',
                                                                is_scatter_geo=True,
                                                                sort_ascending=True)

    return figure_02


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE, host=SERVER_HOST, port=SERVER_PORT)
