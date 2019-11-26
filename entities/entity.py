# -*- coding: utf-8 -*-

"""
Implements parent class for SAP entities.
"""

__author__ = 'Alexey Elizarov (alexei.elizarov@gmail.com)'


class Entity:
    """
    Parent class for SAP entities.
    """
    _query_table = None
    _key_field = None
    _fields = None

    languages = ['RU', 'EN']

    def __init__(self, connection):
        """
        Initializes SAP entity with RFC connection.
        :param connection: RFC connection.
        """
        self._connection = connection

    def __getattr__(self, attr, value=None):
        setattr(self, attr, value)

    def _read_table(self, query_table: str,
                    delimiter: str = '|',
                    no_data: str = '',
                    rowskips: int = 0,
                    rowcount: int = 0,
                    options: str = '',
                    fields: list = None):
        """
        Invokes RFC_READ_TABLE function module via RFC and
        processes returned data.
        :param query_table: Table to read.
        :param delimiter: Sign for indicating field limits in DATA. Default "|".
        :param no_data: If <> SPACE, only FIELDS is filled
        :param rowskips: Skips certain number of rows.
        :param rowcount: Number of rows to read.
        :param options: Selection entries, "WHERE clauses" .
        :param fields: Names (in) and structure (out) of fields to read.
        :return: tuple of data and fields
        """

        _options = [{'TEXT': options.replace('\"', '\'')}]

        if fields is None:
            _fields = []
        else:
            _fields = [{'FIELDNAME': field} for field in fields]

        response = self._connection.call('RFC_READ_TABLE',
                                         QUERY_TABLE=query_table,
                                         DELIMITER=delimiter,
                                         NO_DATA=no_data,
                                         ROWSKIPS=rowskips,
                                         ROWCOUNT=rowcount,
                                         OPTIONS=_options,
                                         FIELDS=_fields)

        _data, _fields = response['DATA'], response['FIELDS']
        _field_names = [field['FIELDNAME'] for field in _fields]

        data = list()

        if _data:
            for item in _data:
                wa = item['WA'].split('|')
                attribs = {key: value.strip() for (key, value) in zip(_field_names, wa)}
                data.append(attribs)

        fields = _fields

        return data, fields

    def _get_text_query_table(self):
        """
        Determines text table and check field for a query table.
        :return: A tuple of text table and check field.
        """

        if self._query_table == 'DD02L':
            return 'DD02T', 'TABNAME'
        elif self._query_table == 'DD04L':
            return 'DD04T', 'ROLLNAME'

        query_table = 'DD08L'
        options = f'CHECKTABLE = "{self._query_table}" AND FRKART = "TEXT"'
        data, _ = self._read_table(query_table=query_table, options=options, rowcount=1)

        if data:
            text_query_table = data[0]['TABNAME']
            check_field = data[0]['FIELDNAME']
            return text_query_table, check_field

    def _get_text(self):
        """
        Determines text for the entity.
        :return: Entity text
        """

        try:
            text_query_table, check_field = self._get_text_query_table()
        except TypeError:
            return ''

        query_table = 'DD03L'

        # Get language field
        options = f'TABNAME = "{text_query_table}" AND LANGUFLAG = "X"'
        data, _ = self._read_table(query_table=query_table, options=options, rowcount=1)
        lang_field = data[0]['FIELDNAME']

        # Get text field
        options = f'TABNAME = "{text_query_table}" AND KEYFLAG = ""'
        data, _ = self._read_table(query_table=query_table, options=options, rowcount=1)
        text_field = data[0]['FIELDNAME']

        # Get text
        for language in self.languages:
            query_table = text_query_table
            options = f'{check_field} = "{getattr(self, self.key_field)}" AND {lang_field} = "{language}"'
            data, _ = self._read_table(query_table=query_table, options=options)
            if data:
                return data[0][text_field]

        return ''

    def update(self, attribs):
        """
        Updates attributes of the entity form the given dictionary.
        :param attribs: Dictionary of attributes
        :return: None
        """
        for key, value in attribs.items():
            self.__getattr__(key, value)

    def get(self, fields=None, **options):
        """
        Retrieves entity's data from the SAP with given fields and options and updates entity's attributes.
        :param fields: Fields to return.
        :param options: Key word parameter for _read_table() method.
        :return: None.
        """

        options_list = list()

        for key, value in options.items():
            options_list.append(f'{key.upper()} = "{value}"')

        options = ' AND '.join(options_list)
        data, self._fields = self._read_table(query_table=self._query_table, options=options,
                                              fields=fields, rowcount=1)
        if data:
            self.update(attribs=data[0])

    @property
    def wiki(self):
        """
        Returns entity's name and text.
        :return: Entity's name and text as a list.
        """
        return [self.name, self.text]

    @property
    def text(self):
        """
        Returns entity's text from SAP.
        :return: Entity's text.
        """
        return self._get_text()

    @property
    def key_field(self):
        """
        Returns entity's key field from SAP if not implemented explicitly.
        :return: Entity's key field.
        """

        if not self._key_field:
            query_table = 'DD03L'
            options = f'TABNAME = "{self._query_table}" AND KEYFLAG = "X"'
            data, _ = self._read_table(query_table=query_table, options=options, rowcount=1)
            if data:
                return data[0]['FIELDNAME']
        else:
            return self._key_field

    @property
    def name(self):
        """
        Returns entity's name.
        :return: Entity's name.
        """
        return getattr(self, self.key_field)