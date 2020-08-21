# -*- coding: utf-8 -*-

from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.express as px
from plotly.graph_objects import Figure, Bar

from modules.exception import CatalogDashException
from modules.logging import logging
from modules.utils import colors


# display a larger df on the console
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


##################################################
# layout services
##################################################

def get_table_styles():
    return {
        'style_as_list_view': True,
        'style_table': {
            'maxHeight': '300px',
            'maxWidth': '1000px',
            'overflowY': 'scroll'
        },
        'style_data_conditional': [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'gray'
            }
        ],
        'style_filter': {
            'backgroundColor': 'white'
        },
        'style_header': {
            'backgroundColor': 'black',
            'fontWeight': 'bold'
        },
        'style_cell': {
            'textAlign': 'left',
            'minWidth': '100px',
            'backgroundColor': 'rgb(65, 65, 65)',
            'color': 'white'
        }
    }


def extra_logging(df):
    logging.info('extra_logging()\n')

    df_copy = df.copy()

    df_copy['year'] = df_copy['date'].map(lambda date: date.year).astype('category')

    # get a list with the available years (e.g. [2016, 2017, 2018, 2019, 2020])
    years = df_copy.year.unique()

    logging.info('extra_logging() - available years: %s\n', years)

    # show the information of the df_copy according to each year
    for year in years:
        df_20xx = df_copy[df_copy['year'] == year]

        # logging.info('extra_logging() - df_%s.head(): \n%s\n', year, df_20xx.head())
        logging.info('extra_logging() - df_%s.shape: %s', year, df_20xx.shape)
        logging.info('extra_logging() - number of datasets in df_%s: %s', year, len(df_20xx.dataset.unique()))
        logging.info('extra_logging() - datasets in df_%s: %s\n', year, df_20xx.dataset.unique())


def get_df_scene_dataset_grouped_by(df_scene_dataset, group_by=['dataset', 'year_month'], sort_by=None):
    # create a copy from the original df_scene_dataset
    # `df_sd` means dataframe scene dataset
    df_sd = df_scene_dataset.copy()

    # extract year_month from my date
    df_sd['year_month'] = df_sd['date'].map(lambda date: date.strftime('%Y-%m'))

    # group the df by `group_by` and count how many scenes are
    df_sd = df_sd.groupby(group_by)['scene_id'].count().to_frame('amount').reset_index()

    # if someone passes `sort_by` parameter, then I sort the values by it
    if sort_by:
        df_sd = df_sd.sort_values(sort_by)

    # I get the last column (i.e. 'amount') and I add it to the beginning
    # Source: https://stackoverflow.com/a/13148611
    columns = df_sd.columns.tolist()
    columns = columns[-1:] + columns[:-1]
    df_sd = df_sd[columns]

    return df_sd


##################################################
# callback services
##################################################

def __get_logical_date_range(df, xaxis_range=None):
    logging.info('__get_logical_date_range()')

    # if there are values, then get a boolean df according to the selected date range
    if xaxis_range:
        # [:-3] - extract the string without the last 3 chars, in other words, I get just the year and month
        start_date = xaxis_range[0][:-3]
        end_date = xaxis_range[1][:-3]

        logging.info('__get_logical_date_range() - start_date: %s', start_date)
        logging.info('__get_logical_date_range() - end_date: %s\n', end_date)

        # extract a boolean df from the original one by the selected date range
        return ((df['year_month'] >= start_date) & (df['year_month'] <= end_date))
    else:
        raise CatalogDashException('Invalid `xaxis_range`, it is empty!')


def get_figure_of_graph_bar_plot_number_of_scenes(df, xaxis_range=[], title=None, animation_frame=None,
                                                  is_scatter_geo=True, sort_ascending=True,
                                                  sort_by=['year_month', 'dataset']):
    logging.info('get_figure_of_graph_bar_plot_number_of_scenes()')

    figure_height = 800
    df_copy = df.copy()

    logging.info('get_figure_of_graph_bar_plot_number_of_scenes() - df_copy.head(): \n%s\n', df_copy.head())
    logging.info('get_figure_of_graph_bar_plot_number_of_scenes() - xaxis_range: %s\n', xaxis_range)

    logical_date_range = __get_logical_date_range(df_copy, xaxis_range)

    # I'm goint to build the `data` parameter of `Figure`
    data = []

    # I would like to build each `bar` based on each dataset
    for dataset in df_copy['dataset'].unique():
        sub_df = df_copy[(df_copy['dataset'] == dataset) & logical_date_range]

        hovertext = 'Number of Scenes: ' + sub_df['amount'].map(str) + '<br>' + \
                    'Period: ' + sub_df['year_month'].map(str) + '<br>' + \
                    'Dataset: ' + sub_df['dataset'].map(str)

        data.append(
            Bar(
                {
                    'x': sub_df['year_month'],
                    'y': sub_df['amount'],
                    'name': dataset,
                    'text': sub_df['amount'],  # text inside the bar
                    'textposition': 'auto',
                    'hovertext': hovertext,
                }
            )
        )

    fig = Figure(
        {
            'data': data,
            'layout': {
                'title': title,
                'xaxis': {'title': 'Period'},
                'yaxis': {'title': 'Number of scenes'},
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )

    fig.update_layout(barmode='group', height=figure_height, xaxis_tickangle=-45)

    return fig


def get_figure_of_graph_bubble_map_number_of_scenes(df, xaxis_range=[], title=None, animation_frame=None,
                                                    is_scatter_geo=True, sort_ascending=True,
                                                    sort_by=['year_month', 'dataset']):
    logging.info('get_figure_of_graph_bubble_map_number_of_scenes()\n')

    figure_height = 800
    df_copy = df.copy()

    logging.info('get_figure_of_graph_bubble_map_number_of_scenes() - df_copy.head(): \n%s\n', df_copy.head())
    logging.info('get_figure_of_graph_bubble_map_number_of_scenes() - xaxis_range: %s\n', xaxis_range)

    logical_date_range = __get_logical_date_range(df_copy, xaxis_range)

    # get a sub set from the df according to the selected date range
    df_copy = df_copy[logical_date_range]

    # sort by date and dataset
    df_copy.sort_values(by=sort_by, ascending=sort_ascending, inplace=True)

    # choose the map type based on the passed flag
    if is_scatter_geo:
        # create a figure using `px.scatter_geo`
        fig = px.scatter_geo(
            df_copy,
            title=title,
            lon='longitude',
            lat='latitude',
            color='dataset',
            size='amount',
            hover_data=['year_month'],
            animation_frame=animation_frame,
            projection='natural earth',
            height=figure_height
        )

        # update the flag
        fig.update_geos(
            showcountries=True,
            bgcolor=colors['background'],
            showocean=True,
            oceancolor='#fff'
        )

        fig.update_layout(
            plot_bgcolor= colors['background'],
            paper_bgcolor= colors['background'],
            font={
                'color': colors['text']
            }
        )
    else:
        # create a figure using `px.scatter_mapbox`
        fig = px.scatter_mapbox(
            df_copy,
            title=title,
            lon='longitude',
            lat='latitude',
            color='dataset',
            size='amount',
            hover_data=['year_month'],
            animation_frame=animation_frame,
            zoom=2,
            height=figure_height
        )

        # add as base map the OSM
        fig.update_layout(
            mapbox_style='open-street-map',
            margin={'t': 40, 'r': 5, 'b': 5, 'l': 5}
        )

    return fig
