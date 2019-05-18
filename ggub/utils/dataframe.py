import pandas as pd


def flatten_column(df, column, new_columns_pfx=None):
    df.drop(column, 1).assign(**df["column"].dropna().apply(pd.Series))
    return


def rename_column(df, column, new_name, inplace=True):
    df.rename(columns={column: new_name}, inplace=inplace)
    return
