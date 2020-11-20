# -*- coding: utf-8 -*-

from json import dumps
from datetime import timedelta

from dash_core_components import DatePickerRange, Dropdown, Graph, Input as dcc_Input, Loading
from dash_html_components import Div, H1, H3, P
from dash_table import DataTable
from dash_leaflet import Colorbar, GeoJSON, Map, TileLayer
from dash_leaflet.express import scatter
from numpy import log as np_log
from pandas import DataFrame, to_datetime

from apps.download.service import default_csc, color_prop, csc_map, csc_options, get_minmax_from_df
from apps.service import filter_df_by, get_table_styles
from modules.logging import logging
from modules.model import DatabaseConnection
from modules.utils import colors


##################################################
# get the dataframes from database
##################################################
# database connection
db = DatabaseConnection()

# get the dash download nofbs dataframe (df_dd_nofbs) from the database
# nofbs - number of downloaded assets by scene
df_dd_nofbs = db.select_from_dash_download_nofbs()


##################################################
# fix the dataframes
##################################################

# convert `str` to a `datetime`, and `datetime` to 'date' type
# df_dd_nofbs['date'] = to_datetime(df_dd_nofbs['date']).dt.date

logging.info(
    "download.layout - df_dd_nofbs.head(): \n"
    f"{df_dd_nofbs[['scene_id', 'nofbs', 'user_id', 'date', 'longitude', 'latitude']].head()}\n"
)
# logging.debug(
#     f"download.layout - df_dd_nofbs.dtypes: \n{df_dd_nofbs.dtypes}\n"
# )

##################################################
# get values from dataframe
##################################################

# get the minimum and maximum dates, and the number of downloaded assets
min_start_date = df_dd_nofbs['date'].min()
max_end_date = df_dd_nofbs['date'].max()
number_of_downloaded_assets = df_dd_nofbs['nofbs'].sum()

logging.info(f'download.layout - min_start_date: {min_start_date}')
logging.info(f'download.layout - max_end_date: {max_end_date}')
logging.info(f'download.layout - number_of_downloaded_assets: {number_of_downloaded_assets}')


# create the information dataframe
data = [
    ['Number of downloaded scenes', len(df_dd_nofbs)],
    ['Number of downloaded assets', number_of_downloaded_assets],
    ['Minimum date', min_start_date],
    ['Maximum date', max_end_date]
]
df_information = DataFrame(data, columns=['information', 'value'])

logging.info(f'download.layout - df_information.head(): \n{df_information.head()}\n')


# df_d_base - number of downloaded scenes by user, date and long/lat
# this df contains all columns I need to build the tables and charts
df_d_base = filter_df_by(
    df_dd_nofbs,
    group_by=['user_id', 'name', 'date', 'longitude', 'latitude'],
    sort_by=['number'],
    ascending=False
)

logging.info(f'download.layout - df_d_base.head(): \n{df_d_base.head()}\n')


minmax = get_minmax_from_df(df_d_base)


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
                    fixed_rows={'headers': True, 'data': 0},
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
                        max_date_allowed=max_end_date + timedelta(days=1),
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
                    children='Limit (max. 1000):',
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
                    placeholder="Limit (max. 1000)",
                    value=100,
                    min=1,
                    max=1000
                )
            ], style={'padding': '10px'}),
        ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    ], style={'padding': '10px'}),

    # tables
    Div([
        # left div - table number of downloaded scenes by date
        Div([
            # title
            P(
                children='Table: Number of Downloaded Scenes by date',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of download scenes
            DataTable(
                id='download--table--number-of-downloaded-scenes-by-date',
                columns=[{"name": i, "id": i} for i in ('number', 'date')],
                data=[],
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=50,
            ),
        ], style={'width': '30%', 'padding': '10px'}),

        # right div - table number of downloaded scenes by user and date
        Div([
            # title
            P(
                children='Table: Number of Downloaded Scenes by user and date',
                style={
                    'textAlign': 'center',
                    'color': colors['text']
                }
            ),
            # table number of download scenes
            DataTable(
                id='download--table--number-of-downloaded-scenes-by-user-and-date',
                columns=[{"name": i, "id": i} for i in ('number', 'user_id', 'name', 'date')],
                data=[],
                fixed_rows={ 'headers': True, 'data': 0 },
                **get_table_styles(),
                sort_action='native',
                sort_mode='multi',
                filter_action='native',
                page_size=50,
            ),
        ], style={'width': '70%', 'padding': '10px'})
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),

    # graph
    Loading(
        id="download--loading--graph--time-series--number-of-downloaded-scenes-by-date",
        type="circle",
        color=colors['text'],
        children=[
            Graph(id='download--graph--graph--time-series--number-of-downloaded-scenes-by-date')
        ]
    ),

    # map
    Loading(
        id="download--loading--map--number-of-downloaded-scenes-by-location",
        type="circle",
        color=colors['text'],
        children=[
            # leaflet map - my code
            Div([
                # title
                P(
                    children='Map: Number of Downloaded Scenes by Location (long/lat)',
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
                            id="download--map--number-of-downloaded-scenes-by-location",
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
                )
                ]
                # style={'width': '100%', 'height': '100vh', 'margin': "auto", "display": "block"}
            )
        ]
    )
])
