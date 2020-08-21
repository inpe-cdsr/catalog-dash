# -*- coding: utf-8 -*-

from dash_core_components import Link
from dash_html_components import Br, Div, H1, H3

from app import url_base_pathname
from modules.utils import colors


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
        children='Index',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    Link('Scene', href='{}/scene'.format(url_base_pathname)),
    Br(),
    Link('Download', href='{}/download'.format(url_base_pathname))
])
