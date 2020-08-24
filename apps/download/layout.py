# -*- coding: utf-8 -*-

from dash_core_components import Graph, DatePickerRange
from dash_html_components import Div, P, H1, H3
from dash_table import DataTable
from pandas import DataFrame

from app import app, url_base_pathname
from apps.service import filter_df_by, get_table_styles
from modules.logging import logging
from modules.model import DatabaseConnection
from modules.utils import colors


# database connection
db = DatabaseConnection()

# create the download dataframe from the Download table in the database
df_download = db.select_from_download()

logging.info('download.layout - df_download.head(): \n%s\n', df_download.head())


# get them minimum and maximum dates
min_start_date = df_download['date'].min()  # min_start_date: 2020-06-29 16:44:46
max_end_date = df_download['date'].max()  # max_end_date: 2020-08-07 15:30:33

logging.info('download.layout - min_start_date: %s', min_start_date)
logging.info('download.layout - max_end_date: %s', max_end_date)


# create a df with the information from `df_download`
data = [
    ['Number of downloaded scenes', len(df_download)],
    ['Minimum date', min_start_date.date()],
    ['Maximum date', max_end_date.date()]
]
df_information = DataFrame(data, columns=['information', 'value'])

logging.info('download.layout - df_information.head(): \n%s\n', df_information.head())


# I group my df by `scene_id` and `year_month` to build the table
df_d_scene_id_year_month = filter_df_by(
    df_download,
    group_by=['scene_id', 'year_month'],
    sort_by=['year_month', 'scene_id'],
    ascending=False
)

logging.info('download.layout - df_d_scene_id_year_month.head(): \n%s\n', df_d_scene_id_year_month.head())

# I group my df by `user_id`, `scene_id` and `year_month` to build the table
df_d_user_id_scene_id_year_month = filter_df_by(
    df_download,
    group_by=['user_id', 'scene_id', 'year_month'],
    sort_by=['year_month', 'user_id', 'scene_id'],
    ascending=False
)

logging.info('download.layout - df_d_user_id_scene_id_year_month.head(): \n%s\n', df_d_user_id_scene_id_year_month.head())


layout = Div([
    # title
    H1(
        children='catalog-dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    # subtitle
    H3(
        children='Download table analysis',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # information table
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
        Div([
            Div([
                DataTable(
                    id='table--information',
                    columns=[{"name": i, "id": i} for i in df_information.columns],
                    data=df_information.to_dict('records'),
                    fixed_rows={ 'headers': True, 'data': 0 },
                    **get_table_styles()
                ),
            ], style={'max-width': '500px'}),
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

        # Select the start and end date to organize the map
        P(
            children='Select the start and end date to organize the charts:',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'margin-top': '20px'
            }
        ),
        # date picker range
        Div([
            Div([
                DatePickerRange(
                    id='download--date-picker-range',
                    display_format='DD/MM/YYYY',
                    min_date_allowed=min_start_date,
                    max_date_allowed=max_end_date,
                    start_date=min_start_date,
                    end_date=max_end_date
                )
            ], style={'padding-right': '10px'}),
            P(
                id='download--output-container-date-picker-range',
                style={
                    'textAlign': 'center',
                    'color': colors['text'],
                    'margin-top': '5px'
                }
            ),
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    ], style={'padding': '10px'}),

    # tables
    Div([
        # left div - table number of downloaded scenes
        Div([
            # title
            P(
                children='Table: Number of Downloaded Scenes by scene_id and year_month',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of download scenes
            DataTable(
                id='table--number-of-downloaded-scenes',
                columns=[{"name": i, "id": i} for i in df_d_scene_id_year_month.columns],
                data=df_d_scene_id_year_month.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=50,
            ),
        ], style={'width': '40%', 'padding': '10px'}),

        # right div - table number of downloaded scenes by user
        Div([
            # title
            P(
                children='Table: Number of Downloaded Scenes by user_id, scene_id and year_month',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of download scenes
            DataTable(
                id='table--number-of-downloaded-scenes',
                columns=[{"name": i, "id": i} for i in df_d_user_id_scene_id_year_month.columns],
                data=df_d_user_id_scene_id_year_month.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=50,
            ),
        ], style={'width': '60%', 'padding': '10px'})
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'})
])
