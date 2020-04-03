# -*- coding: utf-8 -*-

from dash import Dash
from dash_html_components import Div, H1

from catalog_dash.components import get_graph_amount_of_scenes
from catalog_dash.environment import DEBUG_MODE
# from catalog_dash.log import logging
from catalog_dash.model import DatabaseConnection
from catalog_dash.utils import colors, external_stylesheets


app = Dash(__name__, external_stylesheets=external_stylesheets)
db = DatabaseConnection()

df = db.select_from_graph_amount_scenes_by_dataset_and_date()

# print('\n df: \n', df.head())
# print('\n dtypes: \n', df.dtypes)
# print('\n dataset: ', df.dataset.unique())
# print('\n CBERS4A_MUX_L2_DN: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN'].head())
# print('\n date: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['date'].head())
# print('\n amount: : \n', df[df['dataset'] == 'CBERS4A_MUX_L2_DN']['amount'].head())


app.layout = Div(style={'backgroundColor': colors['background']}, children=[
    H1(
        children='catalog-dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    get_graph_amount_of_scenes(df)
])


if __name__ == '__main__':
    app.run_server(debug=DEBUG_MODE)
