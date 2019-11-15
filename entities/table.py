from entities import Entity


class Table(Entity):
    """
    Table
    """
    _query_table = 'DD02L'
    _key_field = 'TABNAME'