#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, url_base_pathname
from apps import *

from modules.environment import DEBUG_MODE, SERVER_HOST, SERVER_PORT
from modules.logging import logging


logging.info('main.py - DEBUG_MODE: %s', DEBUG_MODE)
logging.info('main.py - SERVER_HOST: %s', SERVER_HOST)
logging.info('main.py - SERVER_PORT: %s\n', SERVER_PORT)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '{}/'.format(url_base_pathname):
        return layout_index
    if pathname == '{}/download'.format(url_base_pathname):
        return layout_download
    elif pathname == '{}/scene'.format(url_base_pathname):
        return layout_scene
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE, host=SERVER_HOST, port=SERVER_PORT)
