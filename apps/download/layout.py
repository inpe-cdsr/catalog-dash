# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html

from app import app, url_base_pathname

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
