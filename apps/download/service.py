# -*- coding: utf-8 -*-

from datetime import datetime as dt
from json import dumps

from dash_leaflet.express import dicts_to_geojson


##################################################
# layout services
##################################################

####################
# how to create arrows
####################

# polyline_colors = ['blue', 'red', 'yellow', 'green', 'orange', 'purple', 'black', 'gray']
# i_color = 0

# def get_color():
#     global i_color

#     if i_color >= len(polyline_colors)-1:
#         i_color = 0
#     else:
#         i_color += 1

#     return polyline_colors[i_color]

# arrows = []

# for x in range(-180, 180):
#     color = get_color()

#     arrows.append(
#         dl.PolylineDecorator(
#             children=dl.Polyline(
#                 # positions=[[50, -19], [55, -12]]
#                 positions=[[x, x-30], [x+5, x-40]],
#                 color=color
#             ),
#             patterns=[
#                 dict(
#                     offset='100%',
#                     repeat='0',
#                     arrowHead=dict(
#                         pixelSize=15,
#                         polygon=False,
#                         pathOptions=dict(
#                             stroke=True,
#                             color=color
#                         ),
#                     ),
#                 )
#             ]
#         )
#     )

####################
# dash-leaflet map options
####################

# setup a few color scales.
csc_map = {
    "Hot": ['yellow', 'red', 'black'],
    "Viridis": "Viridis",
    "Rainbow": ['red', 'yellow', 'green', 'blue', 'purple']
}
csc_options = [
    dict(label=key, value=dumps(csc_map[key])) for key in csc_map
]
default_csc = "Hot"

color_prop='number'


def get_minmax_from_df(df, key='number'):
    # return {
    #     'min': np_log(df[key].min()),
    #     'max': np_log(df[key].max())
    # }
    return {
        'min': df[key].min(),
        'max': df[key].max()
    }


##################################################
# callback services
##################################################

def __convert_dates_from_str_to_date(start_date, end_date):
    # convert the [start|end]_date from str to date
    start_date = dt.strptime(start_date.split('T')[0], '%Y-%m-%d').date()
    end_date = dt.strptime(end_date.split('T')[0], '%Y-%m-%d').date()

    return start_date, end_date


def __create_sub_df_based_on_parameters(df, start_date, end_date, limit):
    # get a sub set from the df according to the selected date range
    sub_df = df[
        ((df['date'] >= start_date) & (df['date'] <= end_date))
    ]

    # reset the indexes to avoid the pandas warning related to SettingWithCopyWarning
    sub_df.reset_index(drop=True, inplace=True)

    # return the elements based on the limit, if it is possible
    if limit > 0 and limit < len(sub_df.index):
        sub_df = sub_df.iloc[:limit]

    sub_df['date'] = sub_df['date'].astype(str)

    return sub_df


def __get_geojson_data(df):
    # create a tooltip and popup
    df['tooltip'] = df.apply(
        lambda row: '({}, {})'.format(row["latitude"], row["longitude"]),
        axis=1
    )
    df['popup'] = df.apply(
        lambda row: '''
            User ID: {}<br>
            Number: {}<br>
            Date: {}<br>
            Latitude: {}<br>
            Longitude: {}
        '''.format(
            row["user_id"], row["number"], row["date"], row["latitude"], row["longitude"]
        ),
        axis=1
    )

    # create the markers based on the dataframe
    geojson = dicts_to_geojson(df.to_dict('rows'), lat="latitude", lon="longitude")

    return geojson
