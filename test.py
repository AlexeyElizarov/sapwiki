from pysap import SAP
import selections
import entities
import pages

profile = r"D:\PyProjects\pySAP\profiles\plaut_demo.ini"
# profile = r"D:\PyProjects\pySAP\profiles\haier_dev.ini"
sap = SAP(profile)


def test_connection():
    print(sap.connection.alive)


def test_component():
    component = entities.Component(sap)
    component.get(ps_posid='SLL-ITR-TRC')
    print(component.text)

    for package in component.packages:
        print(package.text)


def test_package():
    package = entities.Package(sap)
    package.get(fields=['DEVCLASS', 'COMPONENT'], devclass='AD01')

    # for repo in package.directory:
    #     print(repo.__dict__)

    for dtel in package.directory.data_elements:
        print(dtel.text)


def test_packages():
    packages = selections.Packages(sap)
    packages.get(fields=['DEVCLASS', 'COMPONENT'], component='/SAPSLL/ER91000643')

    for package in packages:
        print(package.text)


def test_repository_object():
    repo = entities.RepositoryObject(sap)
    repo.get(obj_name='/SAPSLL/TUOMS')
    print(repo.text)


def test_directory():
    directory = selections.Directory(sap)
    directory.get(devclass='/SAPSLL/CORE')

    # for repo in directory:
    #     print(repo.PGMID, repo.OBJECT, repo.OBJ_NAME)

    # for selection in directory._selections:
    #     print(selection)
    #     for obj in getattr(directory, selection)[:2]:
    #         print('\t', obj.name, '\t', obj.text)

    for obj in directory.views:
        print('\t', obj.name, '\t', obj.text)


def test_data_element():
    dtel = entities.DataElement(sap)
    dtel.get(rollname='/SAPSLL/CGRCO')
    print(dtel.text)


def test_auth_object_class():
    auth_object_class = entities.AuthObjectClass(sap)
    auth_object_class.get(oclss='J3RF')

    # for auth_object in auth_object_class.auth_objects:
    #     print(auth_object.name, '\t', auth_object.text)
    #     for check_field in auth_object.check_fields:
    #         print('\t', check_field.name, '\t',  check_field.text)

    for auth_object in auth_object_class.auth_objects:
        print(auth_object.name, '\t', auth_object.text)
        for activity in auth_object.valid_activities:
            print('\t', activity.name, activity.text)


def test_get_key_field():
    obj = entities.DataElement(sap)
    print(obj.get_key_field())


def test_wiki_auth():
    component = entities.Component(sap)
    component.get(ps_posid='SLL-ITR-CLS')
    page = pages.Component(component)
    auth = page.authorizations
    auth.overview()


def test_function_group():
    fg = entities.FunctionGroup(sap)
    fg.get(area='/SAPSLL/API_COMCO_DISTR')

    for fm in fg.function_modules:
        print(fm.wiki)


def test_wiki_functions():
    component = entities.Component(sap)
    component.get(ps_posid='CA-LT')
    page = pages.Component(component)
    page.functions.overview()


def test_wiki_transactions():
    component = entities.Component(sap)
    # component.get(ps_posid='CA-LT')
    component.get(ps_posid='CA-GTF-OC')
    # component.get(ps_posid='MM-IV')
    page = pages.Component(component)
    page.transactions.overview()


def test_transactions():
    component = entities.Component(sap)
    component.get(ps_posid='MM-IV')

    for pckg in component.packages:
        print(pckg.name)
        for transaction in pckg.directory.transactions:
            print('\t', transaction.name)


if __name__ == '__main__':
    # test_connection()
    # test_component()
    # test_packages()
    # test_package()
    # test_repository_object()
    # test_directory()
    # test_data_element()
    # test_auth_object_class()
    # test_get_key_field()
    # test_wiki_auth()
    # test_function_group()
    # test_wiki_functions()
    test_wiki_transactions()
    # test_transactions()



