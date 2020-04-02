# -*- coding: utf-8 -*-

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

from catalog_dash.model import DatabaseConnection
from catalog_dash.log import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)


db = DatabaseConnection()

df_results = db.select_from_graph_amount_scenes_by_dataset_and_date()


df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

print('\n df: \n', df.head())
print('\n continents: ', df.continent.unique())
print('\n Europe: : \n', df[df['continent'] == 'Europe'].head())
print('\n gdp per capita: : \n', df[df['continent'] == 'Europe']['gdp per capita'].head())
print('\n life expectancy: : \n', df[df['continent'] == 'Europe']['life expectancy'].head())
print('\n country: : \n', df[df['continent'] == 'Europe']['country'].head())

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                dict(
                    x=df[df['continent'] == i]['gdp per capita'],
                    y=df[df['continent'] == i]['life expectancy'],
                    text=df[df['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                ) for i in df.continent.unique()
            ],
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                yaxis={'title': 'Life Expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
