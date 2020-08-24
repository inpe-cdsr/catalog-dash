# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from pandas import DataFrame

from app import app, url_base_pathname
from apps.service import filter_df_by
from modules.logging import logging
from modules.model import DatabaseConnection


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


# I group my df by 'scene_id' and 'year_month' to build the table
df_d_scene_id_year_month = filter_df_by(
    df_download,
    group_by=['scene_id', 'year_month'],
    sort_by=['year_month', 'scene_id'],
    ascending=False
)

logging.info('download.layout - df_d_scene_id_year_month.head(): \n%s\n', df_d_scene_id_year_month.head())


layout = html.Div([
    html.H3('Download'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'Download - {}'.format(i), 'value': i} for i in [
                'ABC', 'DFG', 'HIJ'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Scene', href='{}/scene'.format(url_base_pathname))
])
