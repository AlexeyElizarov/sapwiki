from entities.entity import Entity


class Package(Entity):
    """
    Package
    """
    _query_table = 'TDEVC'

    # @property
    # def directory(self):
    #     directory = selections.Directory(self._sap)
    #     directory.get(devclass=self.DEVCLASS)
    #     return directory