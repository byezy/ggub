from abc import ABC, abstractmethod


class WorkspaceDriver(ABC):

    def __init__(self, desc, abbr):
        self.description = desc
        self.abbreviation = abbr

    @abstractmethod
    def create(self, target, **kwargs):
        pass

    @abstractmethod
    def list_data(self, target, **kwargs):
        pass
