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

'''
def get_text(df):
    return 'Amount of Scenes: ' + df['amount'].map(str) + '<br>' + \
            'Dataset: ' + df['dataset'].map(str) + '<br>' + \
            'Year-Month: ' + df['year_month'].map(str) + '<br>' + \
            'Longitude: ' + df['longitude'].map(str) + '<br>' + \
            'Latitude: ' + df['latitude'].map(str)
'''

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
