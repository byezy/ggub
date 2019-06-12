from abc import ABC, abstractmethod
from pathlib import Path
from os import fspath
from os.path import dirname
from importlib import import_module
from pkgutil import iter_modules


class WorkspaceDriver(ABC):

    def __init__(self, desc, abbr):
        self.description = desc
        self.abbreviation = abbr
        return

    @abstractmethod
    def supports(self, workspace):
        pass

    @abstractmethod
    def searchable_objects():
        pass

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def list_data(self, workspace, **kwargs):
        pass


def get_drivers():
    _mpath = Path(__file__)
    driver_module_files = _mpath.parent.glob("ws_*.py")
    driver_modules = [import_module("." + p.stem, package="ggj.geotypes.workspaces") for p in driver_module_files]
    return [getattr(driver_module, 'get_driver')() for driver_module in driver_modules]


drivers = get_drivers()


def get_workspace_driver(workspace):
    ws = fspath(Path(workspace))

    for driver in get_drivers():
        if driver.supports(ws):
            print(f"supported by {driver.description}")
            return driver

    raise ValueError('no driver found for {ws}')


class Searchable(ABC):
    def __init__(self, name, formats):
        self.name = name
        self.formats = formats

    def search(workspace):
        pass



