from tqdm import tqdm
from time import sleep
from pages import Page


class Transactions(Page):
    def __init__(self, component):
        self.component = component

    def overview(self):

        self.resource_id = f'{self.component.PS_POSID}_TRAN'
        self.title = f'{self.component.PS_POSID}_TRAN'

        transactions = []
        user_transactions = []
        cust_transactions = []

        for transaction in tqdm(self.component.transactions, desc='Transactions'):
            transactions.append(transaction.wiki + [transaction.type])

        for transaction in transactions:
            if transaction[2] == 'U':
                user_transactions.append(transaction)
            elif transaction[2] == 'C':
                cust_transactions.append(transaction)

        body = 'h1. Транзакции'
        body += '\n\n{{toc}}'

        if user_transactions:

            self.sort(user_transactions, [0])
            self.format(user_transactions, [0])
            body += '\n\nh2. Пользовательские транзакции'
            body += '\n\n|_.Код транзакции|_.Текст|'

            for transaction in user_transactions:

                line = '|'.join(transaction[:2])
                body += f'\n|{line}|'

        if cust_transactions:

            self.sort(cust_transactions, [0])
            self.format(cust_transactions, [0])
            body += '\n\nh2. Транзакции пользовательской настройки'
            body += '\n\n|_.Код транзакции|_.Текст|'

        for transaction in cust_transactions:

                line = '|'.join(transaction[:2])
                body += f'\n|{line}|'

        sleep(0.5)
        self.text = body
