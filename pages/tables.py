from tqdm import tqdm
from time import sleep
from pages import Page
from collections import defaultdict


class Tables(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        self.resource_id = f'{self.component.PS_POSID}_TABL'
        self.title = f'{self.component.PS_POSID}_TABL'

        tables = []
        tables_by_delclass = defaultdict(list)
        delivery_classes = ['A', 'C', 'E', 'G', 'L', 'S', 'W']
        structures = []
        subtitles = {'A': 'Прикладные таблицы (А)',
                     'C': 'Таблицы пользовательской настройки (С)',
                     'E': 'Управляющие таблицы (E)',
                     'G': 'Таблицы пользовательской настройки (G)',
                     'L': 'Таблицы для хранения временных данных (L)',
                     'S': 'Системные таблицы (S)',
                     'W': 'Системные таблицы (W)'}

        for table in tqdm(self.component.tables, desc='Tables'):
            tables.append(table.wiki + [table.TABCLASS, table.CONTFLAG])

        for table in tables:
            if table[2] == 'INTTAB':
                structures.append(table)
            else:
                tables_by_delclass[table[3]].append(table)

        body = f'h1. Таблицы и структуры'
        body += '\n\n{{toc}}'

        for delivery_class in delivery_classes:
            if tables_by_delclass[delivery_class]:
                body += f'\n\nh2. {subtitles[delivery_class]}'
                table = '\n\n|_.Имя таблицы|_.Текст|_.Вид таблицы ^[1]^|_.Класс поставки ^[2]^|'

                self.sort(tables_by_delclass[delivery_class], [0])
                self.format(tables_by_delclass[delivery_class], [0, 2, 3])

                for tab in tables_by_delclass[delivery_class]:
                    line = '|'.join(tab)
                    table += f'\n|{line}|'

                body += table

        self.sort(structures, [0])
        self.format(structures, [0, 2, 3])

        body += '\n\nh2. Структуры'
        body += '\n\n|_.Имя таблицы|_.Текст|_.Вид таблицы ^[1]^|_.Класс поставки ^[2]^|'

        for structure in structures:
            line = '|'.join(structure)
            body += f'\n|{line}|'

        body += '\n\nh2. Примечания' \
                '\n\n# {{include(PWS_Виды таблиц)}}' \
                '\n# {{include(PWS_Классы_поставки)}}'

        sleep(0.5)
        self.text = body