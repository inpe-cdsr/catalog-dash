# -*- coding: utf-8 -*-

from dash_html_components import Div, H1

from modules.utils import colors


layout_error_404 = Div([
    H1(
        children='404 - Page not found',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    )
])
