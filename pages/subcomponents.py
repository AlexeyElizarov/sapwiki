from tqdm import tqdm
from time import sleep
from pages import Page


class Subcomponents(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        components = []

        for component in tqdm(self.component.subcomponents):
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