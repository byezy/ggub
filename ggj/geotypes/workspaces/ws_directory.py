from .driver import WorkspaceDriver, SupportedObject, SupportedFormat
from ...utils.filesystem import is_directory, create_directory
from collections import OrderedDict


class WorkspaceObject(SupportedObject):
    def __init__(self, *args, **kwargs):
        super(SupportedObject, self).__init__(*args, **kwargs)
        self.formats = [SupportedFormat("Comma Separated Values", "CSV", ".csv"),
                        SupportedFormat("dBase", "dBase", ".dbf")]

    def search(self, workspace):
        for format in self.formats:
            print(format.extension)
        return []


class TableObject(SupportedObject):
    def __init__(self, *args, **kwargs):
        super(SupportedObject, self).__init__(*args, **kwargs)
        self.formats = [SupportedFormat("Comma Separated Values", "CSV", ".csv"),
                        SupportedFormat("dBase", "dBase", ".dbf")]

    def search(self, workspace):
        for format in self.formats:
            print(format.extension)
        return []


class VectorObject(SupportedObject):
    def __init__(self, *args, **kwargs):
        super(SupportedObject, self).__init__(*args, **kwargs)
        self.formats = [SupportedFormat("ESRI Shapefile", "SHP", ".shp")]

    def search(self, workspace):
        return []


class RasterObject(SupportedObject):
    def __init__(self, *args, **kwargs):
        super(SupportedObject, self).__init__(*args, **kwargs)
        self.formats = [SupportedFormat("Geotiff", "GTIFF", ".tif"), SupportedFormat("dBase", "dBase", ".dbf")]

    def search(self, workspace):
        for format in self.formats:
            print(format.extension)
        return []


class OtherObject(SupportedObject):
    def __init__(self, *args, **kwargs):
        super(SupportedObject, self).__init__(*args, **kwargs)
        self.formats = []

    def search(self, workspace):
        for format in self.formats:
            print(format.extension)
        return []


class DirectoryDriver(WorkspaceDriver):

    def supports(self, workspace):
        return is_directory(workspace)

    def searchable_objects(self):
        return OrderedDict((k, v) for k, v in [['workspaces', WorkspaceObject()],
                                               ['tables', TableObject()],
                                               ['rasters', RasterObject()],
                                               ['vectors', VectorObject()],
                                               ['other', OtherObject()]])

    def create(self, **kwargs):
        d = create_directory(kwargs['parent'], kwargs['name'])
        return d

    def list_data(self, workspace, kwargs):
        print(kwargs)
        data = {}
        so = self.searchable_objects()
        sok = so.keys()
        for key in kwargs.keys() - ['recurse']:
            if key in sok:
                data[key] = so[key].search(workspace)
            else:
                print(f"'{key} are not a supported type")

        return data


#     def list_tables():
#         pass

#     def list_rasters():
#         pass

#     def list_vectors():
#         pass

#     def list_other_files():
#         pass


def get_driver():
    return DirectoryDriver("Filesystem Directory", "DIR")

