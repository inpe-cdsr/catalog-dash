# -*- coding: utf-8 -*-

from datetime import datetime as dt
import re

from dash import Dash
from dash_core_components import Dropdown, RadioItems, DatePickerRange
from dash.dependencies import Output, Input
from dash_html_components import Div, H1, H3

from catalog_dash.components import get_graph_amount_of_scenes
from catalog_dash.environment import DEBUG_MODE
from catalog_dash.log import logging
from catalog_dash.model import DatabaseConnection
from catalog_dash.utils import colors, external_stylesheets


app = Dash(__name__, external_stylesheets=external_stylesheets)
db = DatabaseConnection()

df = db.select_from_graph_amount_scenes_by_dataset_and_date()


logging.info('main.py - df.head(): \n%s\n', df.head())
logging.info('main.py - df.shape: %s\n', df.shape)
logging.info('main.py - df.dtypes: \n%s\n', df.dtypes)


start_date = df['date'].min()
end_date = df['date'].max()

logging.info('main.py - start_date: %s', start_date)
logging.info('main.py - end_date: %s', end_date)


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
            min_date_allowed=start_date,
            max_date_allowed=end_date,
            start_date=start_date,
            end_date=end_date
        ),

    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center', 'justify-content': 'center'}),
    H3(
        id='output-container-date-picker-range',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    # main graph
    get_graph_amount_of_scenes(df)
])


@app.callback(
    Output('output-container-date-picker-range', 'children'),
    [Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date')])
def update_output_container_date_picker_range(start_date, end_date):
    # Source: https://dash.plotly.com/dash-core-components/datepickerrange

    string_prefix = ''

    if start_date is not None:
        start_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d')
        start_date_string = start_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '

    if end_date is not None:
        end_date = dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')
        end_date_string = end_date.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string

    if string_prefix == '':
        return 'Select a date to see it displayed here'

    return string_prefix


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE)
