from tqdm import tqdm
from time import sleep


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


class Component:
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


class Transactions(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        transactions = []

        for package in tqdm(self.component.packages):
            for transaction in package.directory.transactions:
                transactions.append(transaction.wiki + [transaction.type])

        self.sort(transactions, [2, 0])
        self.format(transactions, [0, 2])

        body = 'h1. Транзакции'
        body += '\n\n{{toc}}'
        body += '\n\nh2. Пользовательские транзакции'
        body += '\n\n|_.Код транзакции|_.Текст|'

        for transaction in transactions:
            if 'U' in transaction[2]:
                line = '|'.join(transaction[:2])
                body += f'\n|{line}|'

        body += '\n\nh2. Транзакции пользовательской настройки'
        body += '\n\n|_.Код транзакции|_.Текст|'

        for transaction in transactions:
            if 'C' in transaction[2]:
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



