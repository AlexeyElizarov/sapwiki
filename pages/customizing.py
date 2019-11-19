from tqdm import tqdm
from time import sleep
from pages import Page


class Customizing(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        cust = []

        self.resource_id = f'{self.component.PS_POSID}_Пользовательская_настройка'
        self.title = f'{self.component.PS_POSID}_Пользовательская_настройка'

        for actv in tqdm(self.component.customizing, desc='Customizing'):
            cust.append(actv.wiki + [actv.TCODE])

        self.sort(cust, [0])
        self.format(cust, [0, 2])

        body = 'h1. Пользовательская найстрока'
        body += '\n\n|_.Операция IMG|_.Пояснящий текст|_.Транзакция|'

        for actv in cust:
            line = '|'.join(actv)
            body += f'\n|{line}|'

        sleep(0.5)
        self.text = body