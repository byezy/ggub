class WorkspaceFactory:
    def __init__(self):
        pass

class Workspace:
    def __init__(self, desc, abbr, createf, listf):
        self.description = desc
        self.abbreviation = abbr
        self.create_new_function = createf
        self.list_geodata_function = listf