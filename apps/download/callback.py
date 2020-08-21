# -*- coding: utf-8 -*-

from dash.dependencies import Input, Output

from app import app

@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def app2_display_value(value):
    return 'You have selected "{}"'.format(value)
