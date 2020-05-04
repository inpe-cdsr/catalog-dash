# -*- coding: utf-8 -*-

from datetime import datetime as dt
from re import split
from pandas import read_csv, to_datetime, DataFrame

from dash import Dash
from dash_core_components import Graph, DatePickerRange
from dash.dependencies import Output, Input
from dash_html_components import Div, P, H1, H3, H4
from dash_table import DataTable
from flask import Flask, redirect

from catalog_dash.components import get_figure_of_graph_bubble_map_amount_of_scenes, \
                                    get_figure_of_graph_bar_ploy_amount_of_scenes
from catalog_dash.environment import IS_TO_USE_DATA_FROM_DB, DEBUG_MODE, SERVER_HOST, SERVER_PORT
from catalog_dash.exception import CatalogDashException
from catalog_dash.logging import logging
from catalog_dash.model import DatabaseConnection
from catalog_dash.services import get_df_scene_dataset_grouped_by
from catalog_dash.utils import colors, get_table_styles, external_stylesheets, get_formatted_date_as_string, \
                               extra_logging


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
else:
    # get the data from a CSV file
    df_scene_dataset = read_csv('data/scene_dataset.csv')
    df_scene_dataset['date'] = to_datetime(df_scene_dataset['date'])


logging.info('main.py - df_scene_dataset.head(): \n%s\n', df_scene_dataset.head())
# logging.info('main.py - df_scene_dataset.shape: %s\n', df_scene_dataset.shape)
# logging.info('main.py - df_scene_dataset.dtypes: \n%s\n', df_scene_dataset.dtypes)
# logging.info('main.py - type(df_scene_dataset): %s\n', type(df_scene_dataset))

# extra_logging(df_scene_dataset)


# get the values
min_start_date = df_scene_dataset['date'].min()  # min_start_date: 2016-05-01 00:00:00
max_end_date = df_scene_dataset['date'].max()  # max_end_date: 2020-03-03 00:00:00

logging.info('main.py - min_start_date: %s', min_start_date)
logging.info('main.py - max_end_date: %s', max_end_date)


# create a df with the information from `df_scene_dataset`
data = [
    ['Amount of available datasets', len(df_scene_dataset.dataset.unique())],
    ['Amount of records', len(df_scene_dataset)],
    ['Minimum date', min_start_date.date()],
    ['Maximum date', max_end_date.date()]
]
df_information = DataFrame(data, columns=['information', 'value'])

logging.info('main.py - df_information.head(): \n%s\n', df_information.head())


# I group my df by 'dataset' and 'year_month' to build the table
df_sd_dataset_year_month = get_df_scene_dataset_grouped_by(
    df_scene_dataset,
    group_by=['dataset', 'year_month']
)

logging.info('main.py - df_sd_dataset_year_month.head(): \n%s\n', df_sd_dataset_year_month.head())


# I group my df by 'dataset', 'year_month', longitude' and 'latitude' to build the map
df_sd_ds_ym_long_lat = get_df_scene_dataset_grouped_by(
    df_scene_dataset,
    group_by=['dataset', 'year_month', 'longitude', 'latitude'],
    sort_by=['year_month', 'dataset', 'longitude', 'latitude']
)

logging.info('main.py - df_sd_ds_ym_long_lat.head(): \n%s\n', df_sd_ds_ym_long_lat.head())


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
        # left div - table amount of scenes
        Div([
            # title
            P(
                children='Table: Amount of Scenes by Dataset and Year-Month',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table amount of scenes
            DataTable(
                id='table--amount-of-scenes',
                columns=[{"name": i, "id": i} for i in df_sd_dataset_year_month.columns],
                data=df_sd_dataset_year_month.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=50,
            ),
        ], style={'width': '50%', 'padding': '10px'}),

        # right div - information
        Div([
            # title
            P(
                children='Table: Information',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table information
            DataTable(
                id='table--information',
                columns=[{"name": i, "id": i} for i in df_information.columns],
                data=df_information.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles()
            ),

            # Select the start and end date to arrange the map
            P(
                children='Select the start and end date to arrange the charts:',
                style={
                    # 'textAlign': 'left',
                    'color': colors['text'],
                    'margin-top': '20px'
                }
            ),
            # date picker range
            Div([
                DatePickerRange(
                    id='date-picker-range',
                    display_format='DD/MM/YYYY',
                    min_date_allowed=min_start_date,
                    max_date_allowed=max_end_date,
                    start_date=min_start_date,
                    end_date=max_end_date
                )
            ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
            P(
                id='output-container-date-picker-range',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'margin-top': '5px'
                }
            ),
        ], style={'width': '50%', 'padding': '10px'}),
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    # graph--bar-plot--amount-of-scenes
    Graph(id='graph--bar-plot--amount-of-scenes'),

    # graph--bubble-map--amount-of-scenes--with-animation-frame
    Graph(id='graph--bubble-map--amount-of-scenes--with-animation-frame'),

    # graph--bubble-map--amount-of-scenes--without-animation-frame
    # Graph(id='graph--bubble-map--amount-of-scenes--without-animation-frame')
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
    [Output('graph--bar-plot--amount-of-scenes', 'figure'),
    Output('graph--bubble-map--amount-of-scenes--with-animation-frame', 'figure')],
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

    figure_01 = get_figure_of_graph_bar_ploy_amount_of_scenes(df_sd_dataset_year_month,
                                                              xaxis_range=xaxis_range,
                                                              title='Amount of Scenes by Dataset')

    figure_02 = get_figure_of_graph_bubble_map_amount_of_scenes(df_sd_ds_ym_long_lat,
                                                                xaxis_range=xaxis_range,
                                                                title='Amount of Scenes by Dataset in a specific location (long/lat)',
                                                                animation_frame='year_month')

    # figure_03 = get_figure_of_graph_bubble_map_amount_of_scenes(df_sd_ds_ym_long_lat,
    #                                                             xaxis_range=xaxis_range,
    #                                                             title='Amount of Scenes by Dataset in a specific location (long/lat)')

    return figure_01, figure_02


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE, host=SERVER_HOST, port=SERVER_PORT)
