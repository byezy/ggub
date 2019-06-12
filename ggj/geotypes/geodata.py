from os import walk, getcwd
from os.path import join, abspath, isdir
import pandas as pd
from ggj.geotypes.workspaces.driver import get_workspace_driver
from ..utils.filesystem import list_files
from dotmap import DotMap

pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 200)

from osgeo import gdal


class Geodata:
    def __init__(self, workspace, kwargs):
        self.kwargs = kwargs
        self.workspace = workspace
        self.workspace_driver = get_workspace_driver(workspace)
        self.data = None

    def list_data(self):
        for k, v in self.workspace_driver.list_data(self.workspace, self.kwargs).items():
            setattr(Geodata, k, v)


def check_dict_default(dict, key, default):
    if key not in dict:
        dict[key] = default

    return None


def list_geodata(workspace=None, **kwargs):
    if not workspace:
        workspace = getcwd()
        print(f'workspace no specified, using current working directory {workspace}')

    check_dict_default(kwargs, 'recurse', True)
    check_dict_default(kwargs, 'tables', True)
    check_dict_default(kwargs, 'vectors', True)
    check_dict_default(kwargs, 'rasters', True)

    g = Geodata(workspace, kwargs)
    g.list_data()

    return g

# import rasterio

# import warnings

# warnings.filterwarnings("error")


# import subprocess

# print(subprocess.check_output(["gdalmanage", "identify", "-r", "./sample_data"]).decode("UTF-8"))


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


# def get_gdal_framed(path):
#     output = subprocess.check_output(["gdalmanage", "identify", "-r", path]).decode("UTF-8").strip().split("\n")
#     gdal_items = [[item[0].strip(), item[1].strip()] for item in [item.split(":") for item in output]]
#     df = pd.DataFrame(gdal_items, columns=['filename', 'filetype'])
#     df['filename'] = df['filename'].apply(abspath)
#     df.index.names = ["gdal"]
#     return df


# def get_tables(df_gdal):
#     i = df_gdal["filetype"].isin(["CSV"])
#     df_tables = df_gdal[i]
#     df_tables.index.names = ["table"]
#     df_tables.reset_index(inplace=True)
#     return df_tables


# def get_other_framed(df_files, df_gdal):
#     i = df_files["filename"].isin([df_gdal["filename"]])
#     df_other = df_files[~i]
#     df_other.index.names = ["other"]
#     return df_other


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


# class SupportedTypes:
#     def __init__(self):
#         self.workspaces = self.rasters = self.vectors = self.tables = []

#     def supported():
#         gdal_supported = sorted([gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())])
#         self.workspaces = {'GPKG': 'Geopackage', 'DIR': 'File Directory'}  # , 'GDB': 'File Geodatabase'}
#         self.tables = {
#             'CSV': 'Comma Separated Values'}  # , 'TXT': 'Delimited Text', 'DBF': 'dBase Table', 'FGT': 'File Geodatabase Table'}
#         self.vectors = {'SHP': 'ESRI Shapefile'}
