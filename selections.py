import entities


class Selection:
    _query_table = None
    _item = None

    def __init__(self, sap):
        self._sap = sap
        self._items = list()

    def __iter__(self):
        self._i = 0
        return self

    def __next__(self):
        try:
            item = self._items[self._i]
            self._i += 1
            return item
        except IndexError as e:
            raise StopIteration

    def __getitem__(self, item):
        return self._items[item]

    def __len__(self):
        return len(self._items)

    def get(self, fields=None, **options):
        options_list = list()

        for key, value in options.items():
            options_list.append(f'{key.upper()} = "{value}"')

        options = ' AND '.join(options_list)
        data, _ = self._sap.read_table(query_table=self._query_table, options=options, fields=fields)

        for item in data:
            _item = self._item(sap=self._sap)
            _item.update(attribs=item)
            self._items.append(_item)


class Directory(Selection):
    """
    Directory of Repository Objects.
    """

    _query_table = 'TADIR'
    _item = entities.RepositoryObject

    # Object type to entity
    _repo = {'DTEL': entities.DataElement,
             'AUTH': entities.AuthCheckField,
             'SUSO': entities.AuthObject,
             'SUSC': entities.AuthObjectClass,
             'SXSD': entities.BAdI,
             'CLAS': entities.Class,
             'BMFR': entities.Component,
             'ENHS': entities.EnhancementSpot,
             'FUGR': entities.FunctionGroup,
             'CUS0': entities.IMGActivity,
             'SMOD': entities.SAPEnhancement,
             'TABL': entities.Table,
             'TRAN': entities.Transaction,
             'VIEW': entities.View,
             'IWPR': entities.ODataService}

    # Attribute name to object type
    _selections = {'data_elements': 'DTEL',
                   'auth_check_fields': 'AUTH',
                   'auth_objects': 'SUSO',
                   'auth_object_classes': 'SUSC',
                   'badi': 'SXSD',
                   'classes': 'CLAS',
                   'components': 'BMFR',
                   'enhancement_spots': 'ENHS',
                   'function_groups': 'FUGR',
                   'img_activities': 'CUS0',
                   'sap_enhancements': 'SMOD',
                   'tables': 'TABL',
                   'transactions': 'TRAN',
                   'views': 'VIEW',
                   'odata_services': 'IWPR'}

    def __getattr__(self, attrib):

        try:
            object_type = self._selections[attrib]  # Object type
        except KeyError as e:
            raise NameError

        object_list = []  # Object list to return

        for item in self._items:
            if item.OBJECT == object_type:
                try:
                    object_ = self._repo[object_type](self._sap)
                    options = {object_.key_field: item.OBJ_NAME}
                    object_.get(**options)
                    object_list.append(object_)
                except:
                    pass

        return object_list


class Packages(Selection):
    """
    Selection of packages.
    """

    _query_table = 'TDEVC'
    _item = entities.Package


class AuthObjects(Selection):
    """
    Selection of Authorization Objects
    """

    _query_table = 'TOBJ'
    _item = entities.AuthObject


class ValidActivities(Selection):
    """
    Valid activities for each authorization object
    """

    _query_table = 'TACTZ'
    _item = entities.ValidActivity