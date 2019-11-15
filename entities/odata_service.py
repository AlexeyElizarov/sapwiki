from entities.entity import Entity


class ODataService(Entity):
    """
    OData Service
    (R3TR	IWPR	SAP Gateway BSE - Service Builder Project)
    """
    _query_table = '/IWBEP/I_MGW_SRH'
    _key_field = 'TECHNICAL_NAME'
