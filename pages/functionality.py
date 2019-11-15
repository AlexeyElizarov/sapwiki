from tqdm import tqdm
from time import sleep
from pages import Page


class Functionality(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        services = []

        for package in tqdm(self.component.packages):
            for service in package.odata_services:
                services.append(service.wiki)

        self.sort(services, [0])

        body = 'h1. Функции'
        body += '\n\n{{toc}}'

        for service in services:
            body += f'\n\nh2. {service[1]}'
            body += '\n\n*Использование*'
            body += '\n\n*Основные функции*'
            body += '\n\n*Техническая информация*'
            body += f'\n\n|_.Сервис OData|@{service[0]}@|'
            body += f'\n|_.Номер приложения Fiori||'

        sleep(0.5)
        print(body)