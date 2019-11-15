from entities import Entity


class Component(Entity):
    """
    Application Component
    """

    _query_table = 'DF14L'
    _key_field = 'FCTR_ID'

    @property
    def packages(self):

        from entities import Package

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

    @property
    def has_transactions(self):
        for package in self.packages:
            if package.transactions:
                return True
            else:
                continue
        return False

    @property
    def has_odata_services(self):
        for package in self.packages:
            if package.odata_services:
                return True
            else:
                continue
        return False

    @property
    def has_subcomponents(self):
        if self.subcomponents:
            return True
        return False

    @property
    def has_customizing(self):
        for package in self.packages:
            if package.img_activities:
                return True
            else:
                continue
        return False

    @property
    def has_functions(self):
        for package in self.packages:
            if package.function_groups:
                return True
            else:
                continue
        return False

    @property
    def has_tables(self):
        for package in self.packages:
            if package.tables:
                return True
            else:
                continue
        return False