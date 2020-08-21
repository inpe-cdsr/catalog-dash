# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html

from app import app, url_base_pathname


layout = html.Div([
    html.H3('Index'),
    dcc.Link('Scene', href='{}/scene'.format(url_base_pathname)),
    html.Br(),
    dcc.Link('Download', href='{}/download'.format(url_base_pathname))
])
