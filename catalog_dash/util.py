# -*- coding: utf-8 -*-

from catalog_dash.log import logging


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


def get_text(df, dataset):
    sub_df = df[df['dataset'] == dataset]

    # logging.debug('get_text() - sub_df.head(): \n%s\n', sub_df.head())

    concat_df = 'Amount of Scenes: ' + sub_df['amount'].map(str) + '<br>' + \
                'Date: ' + sub_df['date'].map(str) + '<br>' + \
                'Dataset: ' + sub_df['dataset'].map(str)

    # logging.debug('get_text() - concat_df.head(): \n%s\n', concat_df.head())

    return concat_df
