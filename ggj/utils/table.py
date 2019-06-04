import pandas as pd


def flatten_column(df, column, new_columns_pfx=None):
    df.drop(column, 1).assign(**df[column].dropna().apply(pd.Series))
    return


def rename_column(df, column, new_name, inplace=True):
    df.rename(columns={column: new_name}, inplace=inplace)
    return


def apply_function(df, columns_in, function, column_out, kwargs={}):
    df[column_out] = df[columns_in].apply(lambda x: function(*x, **kwargs), axis=1)
    return
