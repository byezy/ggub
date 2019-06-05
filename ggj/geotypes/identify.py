from os import walk
from os.path import join, splitext, abspath
import pandas as pd
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 200)
import fiona
# import rasterio

import warnings
warnings.filterwarnings("error")

import subprocess

# print(subprocess.check_output(["gdalmanage", "identify", "-r", "./sample_data"]).decode("UTF-8"))

class geodata:
    def __init__(self):
        self.files = self.gdal = self.other = self.rasters = self.vectors = self.tables = "Not Set"


# def get_ext(fn):
#     ext = splitext(fn)[1]
#     return ext.lower().strip('.') if format else None


# def is_raster(fn):
#     try:
#         with rasterio.open(fn, 'r') as source:
#             pass
#         return True
#     except:
#         return False


# def is_vector(fn, validate=False):
#     try:
#         with fiona.open(fn, 'r') as source:
#             pass
#         return True
#     except:
#         return False


# def is_table(fn, validate=False):
#     supported_formats = ["csv"]
#     return get_ext(fn) in supported_formats


# def get_datatype(fn):
#     x = is_raster(fn)
#     if x:
#         return x
#     x = is_vector(fn)
#     if x:
#         return x
#     return None


def get_files_framed(path):
    data = [join(abspath(root), filename) for root, dirs, files in walk(path) for filename in files]
    df = pd.DataFrame(data, columns=['filename'])
    df.index.names = ["file"]
    return df


def get_gdal_framed(path):
    output = subprocess.check_output(["gdalmanage", "identify", "-r", path]).decode("UTF-8").strip().split("\n")
    gdal_items = [[item[0].strip(), item[1].strip()] for item in [item.split(":") for item in output]]
    df = pd.DataFrame(gdal_items, columns=['filename', 'filetype'])
    df['filename'] = df['filename'].apply(abspath)
    df.index.names = ["gdal"]
    return df


def get_tables_framed(df_gdal):
    i = df_gdal["filetype"].isin(["CSV"])
    df_tables = df_gdal[i]
    df_tables.index.names = ["table"]
    df_tables.reset_index(inplace=True)
    return df_tables


def get_other_framed(df_files, df_gdal):
    i = df_files["filename"].isin([df_gdal["filename"]])
    df_other = df_files[~i]
    df_other.index.names = ["other"]
    return df_other


# def list_rasters(df):
#     dfr = df.copy()
#     dfr['raster'] = dfr.fullpath.apply(lambda x: is_raster(x))
#     dfr = dfr[dfr.raster==True].reset_index(drop=True)
#     dfr.drop(columns=["raster"], inplace=True)
#     dfr.index += 1
#     dfr.index.names = ["raster"]
#     return dfr


# def list_vectors(df):
#     supported_formats = ["tif"]
#     dfv = df.copy()
#     dfv['vector'] = dfv.filename.apply(lambda x: is_vector(x))
#     dfv = dfv[dfv.vector==True].reset_index(drop=True)
#     dfv.drop(columns=["vector"], inplace=True)
#     dfv.index += 1
#     dfv.index.names = ["vector"]
#     return dfv


# def list_tables(df):
#     supported_formats = ["csv"]
#     dfv = df.copy()
#     dfv['table'] = dfv.filename.apply(lambda x: is_table(x))
#     dfv = dfv[dfv.table==True].reset_index(drop=True)
#     dfv.drop(columns=["table"], inplace=True)
#     dfv.index += 1
#     dfv.index.names = ["table"]
#     return dfv


def list_geodata(path):
    g = geodata()
    g.files = get_files_framed(path)
    g.gdal = get_gdal_framed(path)
    g.tables = get_tables_framed(g.gdal)
    g.other = get_other_framed(g.files, g.gdal)
    print(g.files)
    print(g.gdal)
    print(g.other)
    print(g.tables)
    return g