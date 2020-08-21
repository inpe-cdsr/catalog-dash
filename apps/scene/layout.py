# -*- coding: utf-8 -*-

from dash_core_components import Graph, DatePickerRange
from dash_html_components import Div, P, H1, H3
from dash_table import DataTable
from pandas import read_csv, to_datetime, DataFrame

from app import app, url_base_pathname
from modules.environment import IS_TO_USE_DATA_FROM_DB
from modules.logging import logging
from modules.model import DatabaseConnection
from modules.services import get_df_scene_dataset_grouped_by
from modules.utils import colors


def get_table_styles():
    return {
        'style_as_list_view': True,
        'style_table': {
            'maxHeight': '300px',
            'maxWidth': '1000px',
            'overflowY': 'scroll'
        },
        'style_data_conditional': [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'gray'
            }
        ],
        'style_filter': {
            'backgroundColor': 'white'
        },
        'style_header': {
            'backgroundColor': 'black',
            'fontWeight': 'bold'
        },
        'style_cell': {
            'textAlign': 'left',
            'minWidth': '100px',
            'backgroundColor': 'rgb(65, 65, 65)',
            'color': 'white'
        }
    }


def extra_logging(df):
    logging.info('extra_logging()\n')

    df_copy = df.copy()

    df_copy['year'] = df_copy['date'].map(lambda date: date.year).astype('category')

    # get a list with the available years (e.g. [2016, 2017, 2018, 2019, 2020])
    years = df_copy.year.unique()

    logging.info('extra_logging() - available years: %s\n', years)

    # show the information of the df_copy according to each year
    for year in years:
        df_20xx = df_copy[df_copy['year'] == year]

        # logging.info('extra_logging() - df_%s.head(): \n%s\n', year, df_20xx.head())
        logging.info('extra_logging() - df_%s.shape: %s', year, df_20xx.shape)
        logging.info('extra_logging() - number of datasets in df_%s: %s', year, len(df_20xx.dataset.unique()))
        logging.info('extra_logging() - datasets in df_%s: %s\n', year, df_20xx.dataset.unique())


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
    ['Number of available datasets', len(df_scene_dataset.dataset.unique())],
    ['Number of scenes', len(df_scene_dataset)],
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
        children='Scene table analysis',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # table--number-of-scenes
    Div([
        # left div - table number of scenes
        Div([
            # title
            P(
                children='Table: Number of Scenes by Dataset and Year-Month',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of scenes
            DataTable(
                id='table--number-of-scenes',
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

    # graph--bar-plot--number-of-scenes
    Graph(id='graph--bar-plot--number-of-scenes'),

    # graph--bubble-map--number-of-scenes--with-animation-frame
    Graph(id='graph--bubble-map--number-of-scenes--with-animation-frame'),

    # graph--bubble-map--number-of-scenes--without-animation-frame
    # Graph(id='graph--bubble-map--number-of-scenes--without-animation-frame')
])