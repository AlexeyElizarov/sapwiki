from tqdm import tqdm
from time import sleep
from pages import Page


class Authorizations(Page):

    def __init__(self, component):
        self.component = component

    def overview(self):

        self.resource_id = f'{self.component.PS_POSID}_Полномочия'
        self.title = f'{self.component.PS_POSID}_Полномочия'

        auth_obj_classes = []
        auth_objs = []
        check_fields = []
        activities = []

        for package in tqdm(self.component.packages):
            for auth_obj_class in package.auth_object_classes:
                auth_obj_classes.append(auth_obj_class.wiki)
                for auth_obj in auth_obj_class.auth_objects:
                    auth_objs.append([auth_obj.name] + auth_obj.wiki)
                    for check_field in auth_obj.check_fields:
                        check_fields.append([auth_obj.name] + check_field.wiki)
                    for activity in auth_obj.valid_activities:
                        activities.append([auth_obj.name] + activity.wiki)

        body = 'h1. Полномочия'
        body += '\n\nh2. Классы объектов полномочий'
        body += '\n\n|_.Класс|_.Текст|'

        self.sort(auth_obj_classes, [0])
        self.format(auth_obj_classes, [0])

        for auth_obj_class in auth_obj_classes:
            line = '|'.join(auth_obj_class)
            body += f'\n|{line}|'

        body += '\n\nh2. Объекты полномочий'
        body += '\n\n|_.Класс|_.Объект|_.Текст|'

        self.sort(auth_objs, [1, 0])
        self.format(auth_objs, [0, 1])

        for auth_obj in auth_objs:
            line = '|'.join(auth_obj)
            body += f'\n|{line}|'

        body += '\n\nh2. Поля проверки полномочий'
        body += '\n\n|_.Объект|_.Имя поля|_.Текст|'

        self.sort(check_fields, [1, 0])
        self.format(check_fields, [0, 1])

        for check_field in check_fields:
            line = '|'.join(check_field)
            body += f'\n|{line}|'

        body += '\n\nh2. Операции к объекту полномочий'
        body += '\n\n|_.Объект|_.Операция|_.Текст|'

        self.sort(activities, [1, 0])
        self.format(activities, [0, 1])

        for activity in activities:
            line = '|'.join(activity)
            body += f'\n|{line}|'

        sleep(0.5)
        self.text = body
