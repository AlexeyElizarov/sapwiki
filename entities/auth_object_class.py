from entities import Entity, AuthObject


class AuthObjectClass(Entity):
    """
    Authorization Object Class
    """
    _query_table = 'TOBC'

    @property
    def auth_objects(self):
        auth_objects = []
        query_table = 'TOBJ'
        options = f'OCLSS = "{self.name}"'
        data, _ = self._read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                auth_obj = AuthObject(self._connection)
                auth_obj.get(objct=item['OBJCT'])
                auth_objects.append(auth_obj)

        return auth_objects
