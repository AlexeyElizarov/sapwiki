from time import sleep
from pages import Page, Authorizations, Functions, Transactions, Tables, ODataServices, Subcomponents, Functionality,\
    UserManuals, IDocs, Customizing


class Component(Page):
    def __init__(self, component):
        self.component = component

    @property
    def customizing(self):
        return Customizing(self.component)

    @property
    def idocs(self):
        return IDocs(self.component)

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

    @property
    def functionality(self):
        return Functionality(self.component)

    @property
    def user_manuals(self):
        return UserManuals(self.component)

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

    def describe(self):

        self.resource_id = self.component.PS_POSID
        self.title = self.component.PS_POSID
        self.text = f'h1. {self.component.text}'
        self.text += '\n\nh2. Особенности реализации'
        self.text += '\n\nh3. Проектирование'

        if self.component.has_subcomponents:
            self.text += '\n\n* Компоненты'

        if self.component.has_transactions or self.component.has_odata_services:
            self.text += '\n* Функции'

        self.text += '\n\nh2. Подготовка к промышленной эксплуатации'

        if self.component.has_authorizations:
            self.text += f'\n\n* [[{self.component.PS_POSID}_Полномочия|Полномочия]]'
            self.chapters.append(self.authorizations)

        self.text += '\n\nh3. Реализация'

        if self.component.has_customizing:
            self.text += f'\n\n* [[{self.component.PS_POSID}_Пользовательская настройка|Пользовательская настройка]]'
            # self.chapters.append(self.customizing)

        self.text += '\n\nh2. Примечания'
        self.text += '\n\nh3. Списки\n'

        if self.component.has_idocs:
            self.text += f'\n* [[{self.component.PS_POSID}_IDOC|Базисные типы IDoc]]'
            self.chapters.append(self.idocs)

        if self.component.has_functions:
            self.text += f'\n* [[{self.component.PS_POSID}_FUGR|Группы функций и функциональные модули]]'
            self.chapters.append(self.functions)

        if self.component.has_tables:
            self.text += f'\n* [[{self.component.PS_POSID}_TABL|Таблицы и структуры]]'
            # self.chapters.append(self.tables)

        if self.component.has_transactions:
            self.text += f'\n* [[{self.component.PS_POSID}_TRAN|Транзакции]]'
            # self.chapters.append(self.transactions)

    def directory(self):

        body = f'* *[[{self.component.PS_POSID}|{self.component.text}]]*: '

        components = []
        directory = []
        parent_level = self.component.PS_POSID.count('-')
        output_level = parent_level + 1

        for component in self.component.subcomponents:
            components.append(component)

        for component in components:
            if component.PS_POSID.count('-') == output_level:
                directory.append(f'[[{component.PS_POSID}|{component.text}]]')

        directory.sort()

        body += ' — '.join(directory)

        sleep(0.5)
        print(body)

