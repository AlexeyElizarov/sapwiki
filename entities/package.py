from entities import Entity, DataElement, AuthCheckField, AuthObjectClass, AuthObject, BAdI, Class,\
    Component, EnhancementSpot, FunctionGroup, IMGActivity, SAPEnhancement, Table, Transaction, View, ODataService


class Package(Entity):
    """
    Package
    """
    _query_table = 'TDEVC'

    # Object type to entity
    _repo = {'DTEL': DataElement,
             'AUTH': AuthCheckField,
             'SUSO': AuthObject,
             'SUSC': AuthObjectClass,
             'SXSD': BAdI,
             'CLAS': Class,
             'BMFR': Component,
             'ENHS': EnhancementSpot,
             'FUGR': FunctionGroup,
             'CUS0': IMGActivity,
             'SMOD': SAPEnhancement,
             'TABL': Table,
             'TRAN': Transaction,
             'VIEW': View,
             'IWPR': ODataService}

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

    def _directory(self):
        query_table = 'TADIR'
        options = f'DEVCLASS = "{self.name}"'
        data, _ = self._read_table(query_table=query_table, options=options)
        return data

    def __getattr__(self, attrib, value: str = ''):
        try:
            object_type = self._selections[attrib]  # Object type
        except KeyError as e:
            setattr(self, attrib, value)
            return

        object_list = []  # Object list to return

        for item in self._directory():
            if item['OBJECT'] == object_type:
                try:
                    object_ = self._repo[object_type](self._connection)
                    options = {object_.key_field: item['OBJ_NAME']}
                    object_.get(**options)
                    object_list.append(object_)
                except Exception as e:
                    print(e)

        return object_list

