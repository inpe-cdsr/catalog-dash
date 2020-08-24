# -*- coding: utf-8 -*-

from datetime import datetime as dt
from pandas import set_option

from modules.exception import CatalogDashException
from modules.logging import logging
from modules.utils import get_formatted_date_as_string


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
    # create a copy from the original df
    df_copy = df.copy()

    # extract year_month from my date
    df_copy['year_month'] = df_copy['date'].map(lambda date: date.strftime('%Y-%m'))

    # group the df by `group_by` and count how many scenes are
    df_copy = df_copy.groupby(group_by)['scene_id'].count().to_frame('amount').reset_index()

    # if someone passes `sort_by` parameter, then I sort the values by it
    if sort_by:
        df_copy = df_copy.sort_values(sort_by, ascending=ascending)

    # I get the last column (i.e. 'amount') and I add it to the beginning
    # Source: https://stackoverflow.com/a/13148611
    columns = df_copy.columns.tolist()
    columns = columns[-1:] + columns[:-1]
    df_copy = df_copy[columns]

    return df_copy


##################################################
# callback services
##################################################

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
