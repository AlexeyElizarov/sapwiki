from tqdm import tqdm
from time import sleep
from pages import Page


class Functions(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        self.resource_id = f'{self.component.PS_POSID}_FUGR'
        self.title = f'{self.component.PS_POSID}_FUGR'

        func_groups = []
        func_groups_wiki = []
        func_modules = []
        func_modules_wiki = []

        for func_group in self.component.function_groups:
            func_groups.append(func_group)

        for func_group in tqdm(func_groups, desc='FuncGroups'):
            func_groups_wiki.append(func_group.wiki)

        self.sort(func_groups_wiki, [0])
        self.format(func_groups_wiki, [0])

        for func_group in func_groups:
            for func_module in func_group.function_modules:
                func_modules.append((func_group, func_module))

        for func_module in tqdm(func_modules, desc='FuncModules'):
            func_modules_wiki.append([func_module[0].name] + func_module[1].wiki + [func_module[1].FMODE])

        self.sort(func_modules_wiki, [1, 0])
        self.format(func_modules_wiki, [0, 1, 3])

        body = 'h1. Группы функций и функциональные модули'
        body += '\n\nh2. Функциональные группы'
        body += '\n\n|_.Группа функций|_.Краткий текст|'

        for func_group in func_groups_wiki:
            line = '|'.join(func_group)
            body += f'\n|{line}|'

        body += '\n\nh2. Функциональные модули'
        body += '\n\n|_.Группа функций|_.Функциональный модуль|_.Краткий текст|_.Режим|'

        for func_module in func_modules_wiki:
            line = '|'.join(func_module)
            body += f'\n|{line}|'

        sleep(0.5)
        self.text = body