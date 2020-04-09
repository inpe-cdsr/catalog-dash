# -*- coding: utf-8 -*-

from datetime import datetime as dt
from re import split

from catalog_dash.logging import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def str2bool(value):
    # Source: https://stackoverflow.com/a/715468
    return str(value).lower() in ('true', 't', '1', 'yes', 'y')


def get_text(df):
    # logging.debug('get_text() - df.head(): \n%s\n', df.head())

    concat_df = 'Amount of Scenes: ' + df['amount'].map(str) + '<br>' + \
                'Date: ' + df['date'].map(str) + '<br>' + \
                'Dataset: ' + df['dataset'].map(str)

    # logging.debug('get_text() - concat_df.head(): \n%s\n', concat_df.head())

    return concat_df


def get_formatted_date_as_string(date_string, output_format='%d/%m/%Y'):
    # get the date as datetime
    date = dt.strptime(split('T| ', date_string)[0], '%Y-%m-%d')
    # get the formatted date as string
    return date.strftime(output_format)
