import selections


class Entity:
    """
    Parent class for SAP entities.
    """
    _query_table = None
    _key_field = None
    _fields = None

    def __init__(self, sap):
        self._sap = sap

    def __getattr__(self, attr, value):
        setattr(self, attr, value)

    def _get_text_query_table(self):

        if self._query_table == 'DD02L':
            return 'DD02T', 'TABNAME'
        elif self._query_table == 'DD04L':
            return 'DD04T', 'ROLLNAME'

        query_table = 'DD08L'
        options = f'CHECKTABLE = "{self._query_table}" AND FRKART = "TEXT"'
        data, _ = self._sap.read_table(query_table=query_table, options=options, rowcount=1)

        if data:
            text_query_table = data[0]['TABNAME']
            check_field = data[0]['FIELDNAME']
            return text_query_table, check_field

    def _get_text(self):

        try:
            text_query_table, check_field = self._get_text_query_table()
        except TypeError:
            return ''

        query_table = 'DD03L'

        # Get language field
        options = f'TABNAME = "{text_query_table}" AND LANGUFLAG = "X"'
        data, _ = self._sap.read_table(query_table=query_table, options=options, rowcount=1)
        lang_field = data[0]['FIELDNAME']

        # Get text field
        options = f'TABNAME = "{text_query_table}" AND KEYFLAG = ""'
        data, _ = self._sap.read_table(query_table=query_table, options=options, rowcount=1)
        text_field = data[0]['FIELDNAME']

        # Get text
        for language in self._sap.languages:
            query_table = text_query_table
            options = f'{check_field} = "{getattr(self, self.key_field)}" AND {lang_field} = "{language}"'
            data, _ = self._sap.read_table(query_table=query_table, options=options)
            if data:
                return data[0][text_field]

        return ''

    def update(self, attribs):
        for key, value in attribs.items():
            self.__getattr__(key, value)

    def get(self, fields=None, **options):

        options_list = list()

        for key, value in options.items():
            options_list.append(f'{key.upper()} = "{value}"')

        options = ' AND '.join(options_list)
        data, self._fields = self._sap.read_table(query_table=self._query_table, options=options,
                                                  fields=fields, rowcount=1)
        self.update(attribs=data[0])

    @property
    def wiki(self):
        return [self.name, self.text]

    @property
    def text(self):
        return self._get_text()

    @property
    def key_field(self):

        if not self._key_field:
            query_table = 'DD03L'
            options = f'TABNAME = "{self._query_table}" AND KEYFLAG = "X"'
            data, _ = self._sap.read_table(query_table=query_table, options=options, rowcount=1)
            if data:
                return data[0]['FIELDNAME']
        else:
            return self._key_field

    @property
    def name(self):
        return getattr(self, self.key_field)


class Component(Entity):
    """
    Application Component
    """

    _query_table = 'DF14L'
    _key_field = 'FCTR_ID'

    @property
    def packages(self):
        packages = selections.Packages(self._sap)
        packages.get(fields=['DEVCLASS', 'COMPONENT'], component=getattr(self, 'FCTR_ID'))
        return packages

    @property
    def subcomponents(self):
        subcomponents = []
        query_table = 'DF14L'
        options = f'PS_POSID LIKE "{self.PS_POSID}%"'
        data, _ = self._sap.read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                component = Component(self._sap)
                component.get(fctr_id=item['FCTR_ID'])
                subcomponents.append(component)

        return subcomponents


class DataElement(Entity):
    """
    Data Element
    """
    _query_table = 'DD04L'
    _key_field = 'ROLLNAME'


class Package(Entity):
    """
    Package
    """
    _query_table = 'TDEVC'

    @property
    def directory(self):
        directory = selections.Directory(self._sap)
        directory.get(devclass=self.DEVCLASS)
        return directory


class RepositoryObject(Entity):
    """
    Repository Object
    """
    _query_table = 'TADIR'


class AuthObjectClass(Entity):
    """
    Authorization Object Class
    """
    _query_table = 'TOBC'

    @property
    def auth_objects(self):
        auth_objects = selections.AuthObjects(self._sap)
        auth_objects.get(oclss=self.OCLSS)
        return auth_objects


class View(Entity):
    """
    View
    """
    _query_table = 'DD25L'
    _key_field = 'VIEWNAME'


class IMGActivity(Entity):
    """
    IMG-Activity
    """
    _query_table = 'CUS_IMGACH'


class BAdI(Entity):
    """
    Business Add-In - Definitions
    """
    _query_table = 'SXS_ATTR'
    

class Transaction(Entity):
    """
    Transaction
    """
    _query_table = 'TSTC'
    type = 'U'

    @property
    def text(self):
        text = self._get_text()

        if not text:
            self.type = 'C'
            try:
                activity = IMGActivity(self._sap)
                activity.get(tcode=self.TCODE)
                text = activity.text
            except IndexError:
                return text

        return text


class SAPEnhancement(Entity):
    """
    SAP Enhancement
    """
    _query_table = 'MODSAP'
    
    
class EnhancementSpot(Entity):
    """
    Enhancement Spot
    """
    _query_table = 'ENHSPOTOBJ'


class FunctionGroup(Entity):
    """
    Function Group
    """
    _query_table = 'TLIBG'

    @property
    def function_modules(self):
        function_modules = []
        query_table = 'ENLFDIR'
        options = f'AREA = "{self.AREA}"'
        data, _ = self._sap.read_table(query_table=query_table, options=options)

        if data:
            for item in data:
                function_module = FunctionModule(self._sap)
                function_module.get(funcname=item['FUNCNAME'])
                function_modules.append(function_module)

        return function_modules


class Class(Entity):
    """
    Class
    """
    _query_table = 'SEOCLASS'


class Table(Entity):
    """
    Table
    """
    _query_table = 'DD02L'
    _key_field = 'TABNAME'


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
                check_field = AuthCheckField(self._sap)
                check_field.get(fieldname=getattr(self, attrib))
                check_fields.append(check_field)

        return check_fields

    @property
    def valid_activities(self):
        activities = []
        valid_activities = selections.ValidActivities(self._sap)
        valid_activities.get(brobj=self.OBJCT)

        for item in valid_activities:
            activity = Activity(self._sap)
            activity.get(actvt=item.ACTVT)
            activities.append(activity)

        return activities


class AuthCheckField(Entity):
    """
    Authorization Check Field
    """
    _query_table = 'AUTHX'

    @property
    def text(self):
        try:
            data_element = DataElement(self._sap)
            data_element.get(rollname=self.ROLLNAME)
            return data_element.text
        except Exception as e:
            return ''


class ValidActivity(Entity):
    """
    Valid activity
    """
    _query_table = 'TACTZ'


class Activity(Entity):
    """
    Activity
    """
    _query_table = 'TACT'


class FunctionModule(Entity):
    """
    Function Module
    """
    _query_table = 'TFDIR'


class ODataService(Entity):
    """
    OData Service
    (R3TR	IWPR	SAP Gateway BSE - Service Builder Project)
    """
    _query_table = '/IWBEP/I_MGW_SRH'
    _key_field = 'TECHNICAL_NAME'

