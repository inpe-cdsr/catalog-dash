# -*- coding: utf-8 -*-

from json import dumps
from datetime import timedelta

from dash_core_components import DatePickerRange, Dropdown, Graph, Input as dcc_Input, Loading
from dash_html_components import Div, H1, H3, P
from dash_table import DataTable
from dash_leaflet import Colorbar, GeoJSON, Map, TileLayer
from dash_leaflet.express import scatter
from numpy import log as np_log
from pandas import DataFrame

from apps.download.service import default_csc, color_prop, csc_map, csc_options, get_minmax_from_df
from apps.service import filter_df_by, get_table_styles
from modules.logging import logging
from modules.model import DatabaseConnection
from modules.utils import colors


# database connection
db = DatabaseConnection()

# create the download dataframe from the Download table in the database
df_download = db.select_from_download()

df_download['date'] = df_download['date'].dt.date

logging.info(
    'download.layout - df_download.head(): \n%s\n',
    df_download.head()[['id', 'email', 'scene_id', 'date', 'longitude', 'latitude', 'path']]
)


# get the minimum and maximum dates
min_start_date = df_download['date'].min()
max_end_date = df_download['date'].max()

logging.info('download.layout - min_start_date: %s', min_start_date)
logging.info('download.layout - max_end_date: %s', max_end_date)


# create a df with the information from `df_download`
data = [
    ['Number of downloaded scenes', len(df_download)],
    ['Minimum date', min_start_date],
    ['Maximum date', max_end_date]
]
df_information = DataFrame(data, columns=['information', 'value'])

logging.info('download.layout - df_information.head(): \n%s\n', df_information.head())


# I group my df by `scene_id` and `date` to build the table
df_d_scene_id_date = filter_df_by(
    df_download,
    group_by=['scene_id', 'date'],
    sort_by=['amount', 'date', 'scene_id'],
    ascending=False
)

logging.info('download.layout - df_d_scene_id_date.head(): \n%s\n', df_d_scene_id_date.head())

# I group my df by `email`, `scene_id`, `date`, `longitude`, `latitude` to build the graph
df_d_email_scene_id_date = filter_df_by(
    df_download,
    group_by=['email', 'scene_id', 'date', 'longitude', 'latitude'],
    sort_by=['amount', 'date', 'email', 'scene_id'],
    ascending=False
)

logging.info('download.layout - df_d_email_scene_id_date.head(): \n%s\n', df_d_email_scene_id_date.head())

# remove the 'longitude' and 'latitude' information to build the table
df_d_email_without_location = df_d_email_scene_id_date[['amount', 'email', 'scene_id', 'date']]


minmax = get_minmax_from_df(df_d_email_scene_id_date)


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
        # table information, date picker range and limit
        Div([
            # table information
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
            ], style={'max-width': '400px'}),
            # date picker range
            Div([
                # Select the start and end date to filter the tables and charts
                P(
                    children='Select the start and end date to filter the tables and charts:',
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'margin-top': '20px'
                    }
                ),
                # date picker range
                Div([
                    DatePickerRange(
                        id='download--date-picker-range',
                        display_format='DD/MM/YYYY',
                        min_date_allowed=min_start_date,
                        max_date_allowed=max_end_date,
                        start_date=min_start_date,
                        end_date=min_start_date + timedelta(days=7)
                    )
                ], style={
                    'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center',
                    'padding-right': '10px'
                }),
                # date picker range output
                Div([
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
            # limit
            Div([
                # limit
                P(
                    children='Limit (max. 3000):',
                    style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'margin-top': '20px'
                    }
                ),
                # date picker range
                dcc_Input(
                    id="download--input--limit",
                    type="number",
                    placeholder="Limit (max. 3000)",
                    value=100,
                    min=1,
                    max=3000
                )
            ], style={'padding': '10px'}),
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    ], style={'padding': '10px'}),

    # tables
    Div([
        # left div - table number of downloaded scenes
        Div([
            # title
            P(
                children='Table: Number of Downloaded Scenes by scene_id and date',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of download scenes
            DataTable(
                id='download--table--number-of-downloaded-scenes-by-scene_id-date',
                columns=[{"name": i, "id": i} for i in df_d_scene_id_date.columns],
                data=df_d_scene_id_date.to_dict('records'),
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
                children='Table: Number of Downloaded Scenes by email, scene_id and date',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of download scenes
            DataTable(
                id='download--table--number-of-downloaded-scenes-by-email-scene_id-date',
                columns=[{"name": i, "id": i} for i in df_d_email_without_location.columns],
                data=df_d_email_without_location.to_dict('records'),
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=50,
            ),
        ], style={'width': '60%', 'padding': '10px'})
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    # map
    Loading(
        id="download--loading--map--number-of-downloaded-scenes-by-users",
        type="circle",
        color=colors['text'],
        children=[
            # leaflet map - my code
            Div([
                # title
                P(
                    children='Map - Number of Downloaded Scenes by User in a specific location (long/lat)',
                    style={
                        'textAlign': 'left',
                        'color': colors['text']
                    }
                ),
                Map(
                    [
                        # tile layer
                        TileLayer(),
                        # markers
                        GeoJSON(
                            id="download--map--number-of-downloaded-scenes-by-users",
                            cluster=True,  # when true, data are clustered
                            zoomToBounds=True,  # when true, zooms to bounds when data changes
                            clusterToLayer=scatter.cluster_to_layer,  # how to draw clusters
                            zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. cluster) on click
                            options={
                                # how to draw points
                                'pointToLayer': scatter.point_to_layer
                            },
                            superClusterOptions={
                                # adjust cluster size
                                'radius': 150
                            },
                            hideout={
                                'colorscale': csc_map[default_csc],
                                'color_prop': color_prop,
                                **minmax
                            }
                        ),
                        # *arrows,
                        Colorbar(
                            id="download--map--colorbar",
                            colorscale=csc_map[default_csc],
                            width=20,
                            height=150,
                            **minmax
                        )
                    ],
                    zoom=5,
                    center=(-15.0, -55.0),
                    style={'width': '100%', 'height': '80vh', 'margin': "auto", "display": "block"},
                ),
                Div(
                    Dropdown(
                        id="download--map--dropdown--color-scale",
                        options=csc_options,
                        value=dumps(csc_map[default_csc]),
                        clearable=False
                    ),
                    style={"position": "relative", "bottom": "80px", "left": "10px", "z-index": "1000", "width": "200px"}
                ),
                ],
                # style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}
            ),
        ]
    ),

    # graph
    Loading(
        id="download--loading--graph--bubble-map--number-of-downloaded-scenes-by-users",
        type="circle",
        color=colors['text'],
        children=[
            # download--graph--bubble-map--number-of-downloaded-scenes-by-users
            Graph(id='download--graph--bubble-map--number-of-downloaded-scenes-by-users')
        ]
    )
])
