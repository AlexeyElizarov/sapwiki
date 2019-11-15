from entities import Entity


class DataElement(Entity):
    """
    Data Element
    """
    _query_table = 'DD04L'
    _key_field = 'ROLLNAME'