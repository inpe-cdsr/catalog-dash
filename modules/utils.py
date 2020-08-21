# -*- coding: utf-8 -*-

from datetime import datetime as dt
from re import split


colors = {
    'background': 'black',
    'text': '#7FDBFF'
}


def str2bool(value):
    # Source: https://stackoverflow.com/a/715468
    return str(value).lower() in ('true', 't', '1', 'yes', 'y')


def get_formatted_date_as_string(date_string, output_format='%d/%m/%Y'):
    # get the date as datetime
    date = dt.strptime(split('T| ', date_string)[0], '%Y-%m-%d')
    # get the formatted date as string
    return date.strftime(output_format)
