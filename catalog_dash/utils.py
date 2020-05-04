# -*- coding: utf-8 -*-

from datetime import datetime as dt
from re import split

from catalog_dash.logging import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


colors = {
    'background': 'black',
    'text': '#7FDBFF'
}


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


def str2bool(value):
    # Source: https://stackoverflow.com/a/715468
    return str(value).lower() in ('true', 't', '1', 'yes', 'y')


def get_formatted_date_as_string(date_string, output_format='%d/%m/%Y'):
    # get the date as datetime
    date = dt.strptime(split('T| ', date_string)[0], '%Y-%m-%d')
    # get the formatted date as string
    return date.strftime(output_format)


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
        logging.info('extra_logging() - amount of datasets in df_%s: %s', year, len(df_20xx.dataset.unique()))
        logging.info('extra_logging() - datasets in df_%s: %s\n', year, df_20xx.dataset.unique())


def get_logical_date_range(df, xaxis_range=None):
    logging.info('get_logical_date_range()')

    # if there are values, then get a boolean df according to the selected date range
    if xaxis_range:
        # [:-3] - extract the string without the last 3 chars, in other words, I get just the year and month
        start_date = xaxis_range[0][:-3]
        end_date = xaxis_range[1][:-3]

        logging.info('get_logical_date_range() - start_date: %s', start_date)
        logging.info('get_logical_date_range() - end_date: %s\n', end_date)

        # extract a boolean df from the original one by the selected date range
        return ((df['year_month'] >= start_date) & (df['year_month'] <= end_date))
    else:
        raise CatalogDashException('Invalid `xaxis_range`, it is empty!')
