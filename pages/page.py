class Page:

    @staticmethod
    def sort(items: list, columns: list):
        """
        Sorts list of lists (items) by columns ascending.
        :param items: List to sort
        :param columns: Columns to sort
        :return: Sorted list
        """

        for column in columns:
            items.sort(key=lambda x: x[column])

        return items

    @staticmethod
    def format(items: list, columns: list):
        """
        Formats columns.
        :param items: list to format.
        :param columns: columns to format.
        :return:
        """
        for i in range(len(items)):
            for column in columns:
                if items[i][column]:
                    items[i][column] = f'@{items[i][column]}@'

        return items