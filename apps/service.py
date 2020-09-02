# -*- coding: utf-8 -*-

from datetime import datetime as dt
from pandas import set_option
import plotly.express as px

from modules.exception import CatalogDashException
from modules.logging import logging
from modules.utils import colors, get_formatted_date_as_string



# display a larger dataframe on the console
set_option('display.max_rows', 500)
set_option('display.max_columns', 500)
set_option('display.width', 1000)


##################################################
# layout services
##################################################

def get_table_styles():
    return {
        'style_as_list_view': True,
        'style_table': {
            'maxHeight': '300px',
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

'''
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
'''

def filter_df_by(df, group_by=['dataset', 'year_month'], sort_by=None, ascending=True):
    # group the df by `group_by` and count how many scenes are
    df = df.groupby(group_by)['scene_id'].count().to_frame('amount').reset_index()

    # if someone passes `sort_by` parameter, then I sort the values by it
    if sort_by:
        df = df.sort_values(sort_by, ascending=ascending)

    # I get the last column (i.e. 'amount') and I add it to the beginning
    # Source: https://stackoverflow.com/a/13148611
    columns = df.columns.tolist()
    columns = columns[-1:] + columns[:-1]
    df = df[columns]

    return df


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


def __get_date_picker_range_message(start_date, end_date):
    # Source: https://dash.plotly.com/dash-core-components/datepickerrange

    message = ''

    if start_date is not None:
        message += 'Start Date: {} | '.format(get_formatted_date_as_string(start_date))

    if end_date is not None:
        message += 'End Date: {}'.format(get_formatted_date_as_string(end_date))

    if message == '':
        return 'Select a date to see it displayed here'

    return message


def __get_figure_of_graph_bubble_map_number_of_scenes(df, sort_by=None, ascending=True,
                                                      plot_type='scatter_geo', title=None, color=None,
                                                      animation_frame=None, hover_data=None):
    logging.info('get_figure_of_graph_bubble_map_number_of_scenes()')

    figure_height = 800
    df_copy = df.copy()

    # sort by `sort_by`
    df_copy.sort_values(by=sort_by, ascending=ascending, inplace=True)

    logging.info('get_figure_of_graph_bubble_map_number_of_scenes() - df_copy.head(): \n%s\n', df_copy.head())

    if plot_type == 'scatter_geo':
        # create a figure using `px.scatter_geo`
        fig = px.scatter_geo(
            df_copy,
            title=title,
            lon='longitude',
            lat='latitude',
            color=color,
            size='amount',
            hover_data=hover_data,
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

    elif plot_type == 'scatter_mapbox':
        # create a figure using `px.scatter_mapbox`
        fig = px.scatter_mapbox(
            df_copy,
            title=title,
            lon='longitude',
            lat='latitude',
            color=color,
            size='amount',
            hover_data=hover_data,
            animation_frame=animation_frame,
            zoom=2,
            height=figure_height
        )

        # add as base map the OSM
        fig.update_layout(
            mapbox_style='open-street-map',
            margin={'t': 40, 'r': 5, 'b': 5, 'l': 5}
        )

    else:
        raise CatalogDashException('Invalid `plot_type`={}'.format(plot_type))

    return fig
