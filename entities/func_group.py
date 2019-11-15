from entities.entity import Entity
from entities.func_module import FunctionModule


class FunctionGroup(Entity):
    """
    Function Group
    """
    _query_table = 'TLIBG'

    @property
    def function_modules(self):
        function_modules = []
        query_table = 'ENLFDIR'
        options = f'AREA = "{self.name}"'
        data, _ = self._read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                function_module = FunctionModule(self._connection)
                function_module.get(funcname=item['FUNCNAME'])
                function_modules.append(function_module)

        return function_modules

