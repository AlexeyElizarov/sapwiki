from time import sleep
from pages import Page, Authorizations, Functions, Transactions, Tables, ODataServices, Subcomponents, Functionality,\
    UserManuals


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