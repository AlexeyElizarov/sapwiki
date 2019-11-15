from tqdm import tqdm
from time import sleep
from pages import Page


class Functions(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        func_groups = []
        func_modules = []

        for package in tqdm(self.component.packages):
            for func_group in package.function_groups:
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