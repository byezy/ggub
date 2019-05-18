from os import walk
from os.path import join, splitext, abspath
import pandas as pd
# pd.set_option('display.width', 200)
# pd.set_option('display.max_colwidth', 200)


def get_ext(fn):
    ext = splitext(fn)[1]
    return ext.lower().strip('.') if format else None


def is_raster(fn, validate=False):
    supported_formats = ["tif"]
    return get_ext(fn) in supported_formats


def is_vector(fn, validate=False):
    supported_formats = ["shp"]
    return get_ext(fn) in supported_formats


def get_datatype(fn):
    x = is_raster(fn)
    if x:
        return x
    x = is_vector(fn)
    if x:
        return x
    return None


def get_files_framed(path):
    data = [(filename, join(abspath(root), filename)) for root, dirs, files in walk(path) for filename in files]
    df = pd.DataFrame(data, columns=['filename', 'fullpath'])
    return df


# def get_geodata_framed(df):
#     df['datatype'] = df['filename'].apply(get_datatype)
#     return geo_df


def list_rasters(df):
    dfr = df.copy()
    dfr['raster'] = dfr.filename.apply(lambda x: is_raster(x))
    dfr = dfr[dfr.raster==True].reset_index(drop=True)
    dfr.drop(columns=["raster"], inplace=True)
    dfr.index += 1
    dfr.index.names = ["raster"]
    return dfr


def list_vectors(df):
    supported_formats = ["tif"]
    dfv = df.copy()
    dfv['vector'] = dfv.filename.apply(lambda x: is_vector(x))
    dfv = dfv[dfv.vector==True].reset_index(drop=True)
    dfv.drop(columns=["vector"], inplace=True)
    dfv.index += 1
    dfv.index.names = ["vector"]
    return dfv


def list_geodata(path, rasters=False, vectors=False):
    files_df = get_files_framed(path)
    d = {}
    if rasters:
        d['rasters'] = list_rasters(files_df)
    if rasters:
        d['vectors'] = list_vectors(files_df)
    return d
