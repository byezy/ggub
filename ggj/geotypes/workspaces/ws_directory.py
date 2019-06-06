from driver import WorkspaceDriver
from ...utils.filesystem import create_directory


class DirectoryDriver(WorkspaceDriver):

    def create(self, **kwargs):
        d = create_directory(kwargs['parent'], kwargs['name'])
        return d

    def list_data(self, **kwargs):
        pass


driver = DirectoryDriver("Filesystem Directory", "DIR")

