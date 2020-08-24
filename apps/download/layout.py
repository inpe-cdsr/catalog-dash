# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from pandas import DataFrame, set_option

from app import app, url_base_pathname
from modules.logging import logging
from modules.model import DatabaseConnection


# display a larger df on the console
set_option('display.max_rows', 500)
set_option('display.max_columns', 500)
set_option('display.width', 1000)


# database connection
db = DatabaseConnection()

df_download = db.select_from_download()


logging.info('download.layout - df_download.head(): \n%s\n', df_download.head())
# logging.info('download.layout- df_download.shape: %s\n', df_download.shape)
# logging.info('download.layout- df_download.dtypes: \n%s\n', df_download.dtypes)
# logging.info('download.layout- type(df_download): %s\n', type(df_download))

# extra_logging(df_download)

# get the values
min_start_date = df_download['datetime'].min()  # min_start_date: 2020-06-29 16:44:46
max_end_date = df_download['datetime'].max()  # max_end_date: 2020-08-07 15:30:33

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
