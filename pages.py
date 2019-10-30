from tqdm import tqdm
from time import sleep
from collections import defaultdict


class Page:

    @staticmethod
    def sort(items: list, columns: list):
        """
        Sorts list of lists (items) by columns ascending.
        :param items: List to sort
        :param columns: Columns to sort
        :return: Sorted list
        """

        for column in columns:
            items.sort(key=lambda x: x[column])

        return items

    @staticmethod
    def format(items: list, columns: list):
        """
        Formats columns.
        :param items: list to format.
        :param columns: columns to format.
        :return:
        """
        for i in range(len(items)):
            for column in columns:
                if items[i][column]:
                    items[i][column] = f'@{items[i][column]}@'

        return items


class Component(Page):
    def __init__(self, component):
        self.component = component

    @property
    def authorizations(self):
        return Authorizations(self.component)

    @property
    def functions(self):
        return Functions(self.component)

    @property
    def transactions(self):
        return Transactions(self.component)

    @property
    def tables(self):
        return Tables(self.component)

    @property
    def odata_services(self):
        return ODataServices(self.component)

    @property
    def subcomponents(self):
        return Subcomponents(self.component)

    def overview(self):
        body = f'h1. {self.component.text}'
        body += '\n\nh2. Особенности реализации'

        components = []
        parent_level = self.component.PS_POSID.count('-')
        output_level = parent_level + 1

        for component in self.component.subcomponents:
            components.append(component.wiki + [component.PS_POSID])

        self.sort(components, [2])

        for component in components:
            if component[2].count('-') == output_level:
                body += f'\n\nh3. {component[1]}'
                body += f'\n\n_Основная статья: [[{component[2]}|{component[1]}]]_.'
                body += f'\n\nПрикладой компонент "{component[1]}" (@{component[2]}@) обеспечивает следующие функции:'

        sleep(0.5)
        print(body)


class Subcomponents(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        components = []

        for component in self.component.subcomponents:
            components.append(component.wiki + [component.PS_POSID])

        self.sort(components, [2])
        self.format(components, [0, 2])

        body = 'h1. Компоненты'
        body += '\n\n|_.Компонент|_.Краткое описание|_.Прикладной компонент|'

        for component in components:
            line = '|'.join(component)
            body += f'\n|{line}|'

        sleep(0.5)
        print(body)


class ODataServices(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        services = []

        for package in tqdm(self.component.packages):
            for service in package.directory.odata_services:
                services.append(service.wiki)

        body = 'h1. Сервисы OData'
        body += '\n\n|_.Техническое имя|_.Описание|_.Номер приложения Fiori|'

        self.sort(services, [0])
        self.format(services, [0])

        for service in services:
            line = '|'.join(service)
            body += f'\n|{line}||'

        sleep(0.5)
        print(body)


class Tables(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        tables = []
        tables_by_delclass = defaultdict(list)
        delivery_classes = ['A', 'C', 'E', 'G', 'L', 'S', 'W']
        structures = []
        subtitles = {'A': 'Прикладные таблицы (А)',
                     'C': 'Таблицы пользовательской настройки (С)',
                     'E': 'Управляющие таблицы (E)',
                     'G': 'Таблицы пользовательской настройки (G)',
                     'L': 'Таблицы для хранения временных данных (L)',
                     'S': 'Системные таблицы (S)',
                     'W': 'Системные таблицы (W)'}

        for package in tqdm(self.component.packages):
            for table in package.directory.tables:
                tables.append(table.wiki + [table.TABCLASS, table.CONTFLAG])

        for table in tables:
            if table[2] == 'INTTAB':
                structures.append(table)
            else:
                tables_by_delclass[table[3]].append(table)

        body = 'h1. Таблицы и структуры'
        body += '\n\n{{toc}}'

        for delivery_class in delivery_classes:
            if tables_by_delclass[delivery_class]:
                body += f'\n\nh2. {subtitles[delivery_class]}'
                table = '\n\n|_.Имя таблицы|_.Текст|_.Вид таблицы ^[1]^|_.Класс поставки ^[2]^|'

                self.sort(tables_by_delclass[delivery_class], [0])
                self.format(tables_by_delclass[delivery_class], [0, 2, 3])

                for tab in tables_by_delclass[delivery_class]:
                    line = '|'.join(tab)
                    table += f'\n|{line}|'

                body += table

        self.sort(structures, [0])
        self.format(structures, [0, 2, 3])

        body += '\n\nh2. Структуры'
        body += '\n\n|_.Имя таблицы|_.Текст|_.Вид таблицы ^[1]^|_.Класс поставки ^[2]^|'

        for structure in structures:
            line = '|'.join(structure)
            body += f'\n|{line}|'

        body += '\n\nh2. Примечания' \
                '\n\n# {{include(PWS_Виды таблиц)}}' \
                '\n# {{include(PWS_Классы_поставки)}}'

        sleep(0.5)
        print(body)


class Transactions(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        transactions = []
        user_transactions = []
        cust_transactions = []

        for package in tqdm(self.component.packages):
            for transaction in package.directory.transactions:
                transactions.append(transaction.wiki + [transaction.type])

        for transaction in transactions:
            if transaction[2] == 'U':
                user_transactions.append(transaction)
            elif transaction[2] == 'C':
                cust_transactions.append(transaction)

        body = 'h1. Транзакции'
        body += '\n\n{{toc}}'

        if user_transactions:

            self.sort(user_transactions, [0])
            self.format(user_transactions, [0])
            body += '\n\nh2. Пользовательские транзакции'
            body += '\n\n|_.Код транзакции|_.Текст|'

            for transaction in user_transactions:

                line = '|'.join(transaction[:2])
                body += f'\n|{line}|'

        if cust_transactions:

            self.sort(cust_transactions, [0])
            self.format(cust_transactions, [0])
            body += '\n\nh2. Транзакции пользовательской настройки'
            body += '\n\n|_.Код транзакции|_.Текст|'

        for transaction in cust_transactions:

                line = '|'.join(transaction[:2])
                body += f'\n|{line}|'

        sleep(0.5)
        print(body)


class Functions(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        func_groups = []
        func_modules = []

        for package in tqdm(self.component.packages):
            for func_group in package.directory.function_groups:
                func_groups.append(func_group.wiki)
                for func_module in func_group.function_modules:
                    func_modules.append([func_group.name] + func_module.wiki + [func_module.FMODE])

        body = 'h1. Группы функций и функциональные модули'
        body += '\n\nh2. Функциональные группы'
        body += '\n\n|_.Группа функций|_.Краткий текст|'

        self.sort(func_groups, [0])
        self.format(func_groups, [0])

        for func_group in func_groups:
            line = '|'.join(func_group)
            body += f'\n|{line}|'

        body += '\n\nh2. Функциональные модули'
        body += '\n\n|_.Группа функций|_.Функциональный модуль|_.Краткий текст|_.Режим|'

        self.sort(func_modules, [1, 0])
        self.format(func_modules, [0, 1, 3])

        for func_module in func_modules:
            line = '|'.join(func_module)
            body += f'\n|{line}|'

        sleep(0.5)
        print(body)


class Authorizations(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        auth_obj_classes = []
        auth_objs = []
        check_fields = []
        activities = []

        for package in tqdm(self.component.packages):
            for auth_obj_class in package.directory.auth_object_classes:
                auth_obj_classes.append(auth_obj_class.wiki)
                for auth_obj in auth_obj_class.auth_objects:
                    auth_objs.append([auth_obj.name] + auth_obj.wiki)
                    for check_field in auth_obj.check_fields:
                        check_fields.append([auth_obj.name] + check_field.wiki)
                    for activity in auth_obj.valid_activities:
                        activities.append([auth_obj.name] + activity.wiki)

        body = 'h1. Полномочия'
        body += '\n\nh2. Классы объектов полномочий'
        body += '\n\n|_.Класс|_.Текст|'

        self.sort(auth_obj_classes, [0])
        self.format(auth_obj_classes, [0])

        for auth_obj_class in auth_obj_classes:
            line = '|'.join(auth_obj_class)
            body += f'\n|{line}|'

        body += '\n\nh2. Объекты полномочий'
        body += '\n\n|_.Класс|_.Объект|_.Текст|'

        self.sort(auth_objs, [1, 0])
        self.format(auth_objs, [0, 1])

        for auth_obj in auth_objs:
            line = '|'.join(auth_obj)
            body += f'\n|{line}|'

        body += '\n\nh2. Поля проверки полномочий'
        body += '\n\n|_.Объект|_.Имя поля|_.Текст|'

        self.sort(check_fields, [1, 0])
        self.format(check_fields, [0, 1])

        for check_field in check_fields:
            line = '|'.join(check_field)
            body += f'\n|{line}|'

        body += '\n\nh2. Операции к объекту полномочий'
        body += '\n\n|_.Объект|_.Операция|_.Текст|'

        self.sort(activities, [1, 0])
        self.format(activities, [0, 1])

        for activity in activities:
            line = '|'.join(activity)
            body += f'\n|{line}|'

        sleep(0.5)
        print(body)



