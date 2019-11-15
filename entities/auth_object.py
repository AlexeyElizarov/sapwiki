from entities import Entity, AuthCheckField, Activity


class AuthObject(Entity):
    """
    Authorization Object
    """
    _query_table = 'TOBJ'

    @property
    def check_fields(self):
        check_fields = []

        for attrib in dir(self):
            if attrib.startswith('FIEL') and getattr(self, attrib):
                check_field = AuthCheckField(self._connection)
                check_field.get(fieldname=getattr(self, attrib))
                check_fields.append(check_field)

        return check_fields

    @property
    def valid_activities(self):
        valid_activities = []
        query_table = 'TACTZ'
        options = f'BROBJ = "{self.name}"'
        data, _ = self._read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                activity = Activity(self._connection)
                activity.get(actvt=item['ACTVT'])
                valid_activities.append(activity)

        return valid_activities

