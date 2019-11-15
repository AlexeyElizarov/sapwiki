from entities.entity import Entity
from entities.auth_check_field import AuthCheckField


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
