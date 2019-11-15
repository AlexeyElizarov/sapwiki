from tqdm import tqdm
from time import sleep
from pages import Page


class ODataServices(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        services = []

        for package in tqdm(self.component.packages):
            for service in package.odata_services:
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