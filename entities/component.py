from entities.entity import Entity
from entities.package import Package


class Component(Entity):
    """
    Application Component
    """

    _query_table = 'DF14L'
    _key_field = 'FCTR_ID'

    @property
    def packages(self):
        packages = []
        query_table = 'TDEVC'
        options = f'COMPONENT = "{self.name}"'
        data, _ = self._read_table(query_table=query_table, options=options, fields=['DEVCLASS', 'COMPONENT'])

        if data:
            for item in data:
                package = Package(self._connection)
                package.update(item)
                packages.append(package)

        return packages

    @property
    def subcomponents(self):
        subcomponents = []
        query_table = 'DF14L'
        options = f'PS_POSID LIKE "{self.PS_POSID}%"'
        data, _ = self._read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                component = Component(self._connection)
                component.update(item)
                subcomponents.append(component)

        return subcomponents