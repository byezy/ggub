from .driver import WorkspaceDriver, Searchable
from ...utils.filesystem import is_directory, create_directory


class TableSearchable(Searchable):
    def search(workspace):


class DirectoryDriver(WorkspaceDriver):

    def supports(self, workspace):
        return is_directory(workspace)

    def searchable_objects():
        return {'tables': {'formats': list_tables, 'rasters': list_rasters, 'vectors': list_vectors,
                           'other': list_other_files}

    def create(self, **kwargs):
        d = create_directory(kwargs['parent'], kwargs['name'])
        return d

    def list_data(self, workspace, kwargs):
        print(kwargs)
        rasters = kwargs.get('rasters', False)
        print(f"rasters {rasters}")
        return

    def list_tables():
        pass

    def list_rasters():
        pass

    def list_vectors():
        pass

    def list_other_files():
        pass


def get_driver():
    return DirectoryDriver("Filesystem Directory", "DIR")
