# -*- coding: utf-8 -*-

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import plotly.express as px

from catalog_dash.exception import CatalogDashException
from catalog_dash.logging import logging
from catalog_dash.utils import colors, get_text


def get_figure_of_graph_time_series_amount_of_scenes(df, xaxis_range=[]):
    logging.info('get_figure_of_graph_amount_of_scenes()\n')

    logical_date_range = None

    # create the object `layout.xaxis`
    xaxis = {
        'title': 'Date',
        # 'range': ['2018-03-01', '2019-03-03']  # where the `range` key should be
    }

    # if there are values, then do operations with the data, convert it and add it to the figure
    if xaxis_range:
        logging.info('get_figure_of_graph_amount_of_scenes() - inserted xaxis_range: %s\n', xaxis_range)

        # convert [start|end]_date from `str` to `datetime` in order to
        start_date = dt.strptime(xaxis_range[0], '%Y-%m-%d')
        end_date = dt.strptime(xaxis_range[1], '%Y-%m-%d')

        # extract the data from the original selected range
        logical_date_range = ((df['date'] >= start_date) & (df['date'] <= end_date))

        # substract and add months in order to make the graph look better
        start_date -= relativedelta(months=6)
        end_date += relativedelta(months=6)

        # convert the dates from `datetime` to `str` again in order to pass the xaxis range to build the figure
        xaxis_range = [start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')]

        logging.info('get_figure_of_graph_amount_of_scenes() - converted xaxis_range: %s\n', xaxis_range)

        # add the `xaxis_range` to the figure
        xaxis['range'] = xaxis_range

    else:
        raise CatalogDashException('Invalid `xaxis_range`, it is empty!')

    return {
        'data': [
            {
                'x': df[(df['dataset'] == dataset) & (logical_date_range)]['date'],
                'y': df[(df['dataset'] == dataset) & (logical_date_range)]['amount'],
                'text': get_text(df[(df['dataset'] == dataset) & (logical_date_range)]),
                'mode': 'lines+markers',
                'opacity': 0.7,
                'marker': {'size': 7},
                'name': dataset
            } for dataset in df.dataset.unique()
        ],
        'layout': {
            'xaxis': xaxis,
            'yaxis': {'title': 'Amount of scenes'},
            'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
            'legend': {'x': 0, 'y': 1},
            'hovermode': 'closest',
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                'color': colors['text']
            }
        }
    }


def get_figure_of_graph_bubble_map_amount_of_scenes(df, xaxis_range=[]):
    logging.info('get_figure_of_graph_bubble_map_amount_of_scenes()\n')

    import plotly.graph_objects as go

    import pandas as pd

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_us_cities.csv')
    df.head()

    logging.info('get_figure_of_graph_amount_of_scenes() - df.head(): \n%s\n', df.head())

    df['text'] = df['name'] + '<br>Population ' + (df['pop']/1e6).astype(str)+' million'
    limits = [(0,2),(3,10),(11,20),(21,50),(50,3000)]
    colors = ["royalblue","crimson","lightseagreen","orange","lightgrey"]
    cities = []
    scale = 5000

    fig = go.Figure()

    for i in range(len(limits)):
        lim = limits[i]
        df_sub = df[lim[0]:lim[1]]
        fig.add_trace(go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_sub['lon'],
            lat = df_sub['lat'],
            text = df_sub['text'],
            marker = dict(
                size = df_sub['pop']/scale,
                color = colors[i],
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
            ),
            name = '{0} - {1}'.format(lim[0],lim[1])))

    fig.update_layout(
            title_text = '2014 US city populations<br>(Click legend to toggle traces)',
            showlegend = True,
            geo = dict(
                scope = 'usa',
                landcolor = 'rgb(217, 217, 217)',
            )
        )

    return fig
