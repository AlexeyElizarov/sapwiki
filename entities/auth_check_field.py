from entities.entity import Entity
from entities.data_element import DataElement


class AuthCheckField(Entity):
    """
    Authorization Check Field
    """
    _query_table = 'AUTHX'

    @property
    def text(self):
        try:
            data_element = DataElement(self._connection)
            data_element.get(rollname=self.ROLLNAME)
            return data_element.text
        except Exception as e:
            return ''