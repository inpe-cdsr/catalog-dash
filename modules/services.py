# -*- coding: utf-8 -*-

from modules.logging import logging


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
