# -*- coding: utf-8 -*-

from catalog_dash.logging import logging


def get_df_scene_dataset_grouped_by(df_scene_dataset, groupby=['dataset', 'year_month']):
    # create a copy from the original df_scene_dataset
    # `df_sd` means dataframe scene dataset
    df_sd = df_scene_dataset.copy()

    # extract year_month from my date
    df_sd['year_month'] = df_sd['date'].map(lambda date: date.strftime('%Y-%m'))

    # group the df by `groupby` and count how many scenes are
    df_sd = df_sd.groupby(groupby)['scene_id'].count().to_frame('amount').reset_index().sort_values(groupby)

    # I get the last column (i.e. 'amount') and I add it to the beginning
    # Source: https://stackoverflow.com/a/13148611
    columns = df_sd.columns.tolist()
    columns = columns[-1:] + columns[:-1]
    df_sd = df_sd[columns]

    return df_sd
