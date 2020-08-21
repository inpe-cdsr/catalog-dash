#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dash_core_components import Location
from dash.dependencies import Input, Output
from dash_html_components import Div

from app import app, url_base_pathname
import apps

from modules.environment import DEBUG_MODE, SERVER_HOST, SERVER_PORT
from modules.logging import logging


logging.info('main.py - DEBUG_MODE: %s', DEBUG_MODE)
logging.info('main.py - SERVER_HOST: %s', SERVER_HOST)
logging.info('main.py - SERVER_PORT: %s\n', SERVER_PORT)


app.layout = Div([
    Location(id='url', refresh=False),
    Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '{}/'.format(url_base_pathname):
        return apps.layout_index
    if pathname == '{}/download'.format(url_base_pathname):
        return apps.layout_download
    elif pathname == '{}/scene'.format(url_base_pathname):
        return apps.layout_scene
    else:
        return apps.layout_error_404


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE, host=SERVER_HOST, port=SERVER_PORT)
