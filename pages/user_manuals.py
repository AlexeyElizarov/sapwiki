from tqdm import tqdm
from time import sleep
from pages import Page


class UserManuals(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        services = []

        for package in tqdm(self.component.packages):
            for service in package.odata_services:
                services.append(service.wiki)

        self.sort(services, [0])

        body = 'h1. Руководства пользователя'
        body += '\n'

        for service in services:
            body += f'\n* [[UMD_{service[0]}|{service[1]}]]'

        sleep(0.5)
        print(body)
