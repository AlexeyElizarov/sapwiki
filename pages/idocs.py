from tqdm import tqdm
from time import sleep
from pages import Page


class IDocs(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        self.resource_id = f'{self.component.PS_POSID}_IDOC'
        self.title = f'{self.component.PS_POSID}_IDOC'

        idocs = []

        for idoc in tqdm(self.component.idocs, desc='IDocs'):
            idocs.append(idoc.wiki)

        body = 'h1. Базисные типы IDoc'
        body += '\n\n|_.Базисный тип|_.Описание|'

        self.sort(idocs, [0])
        self.format(idocs, [0])

        for idoc in idocs:
            line = '|'.join(idoc)
            body += f'\n|{line}|'

        sleep(0.5)
        self.text = body