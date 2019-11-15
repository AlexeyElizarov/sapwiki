class Page:

    resource_id = None
    title = None
    text = None
    chapters = []

    @staticmethod
    def sort(items: list, columns: list = None):
        """
        Sorts list of lists (items) by columns ascending.
        :param items: List to sort
        :param columns: Columns to sort
        :return: Sorted list
        """

        for column in columns:
            items.sort(key=lambda x: x[column])

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

    def post(self, redmine, **kwargs):
        try:
            redmine.wiki_page.new(project_id=kwargs['project_id'],
                                  title=self.title,
                                  text=self.text)
        except:
            redmine.wiki_page.update(resource_id=self.resource_id,
                                     project_id=kwargs['project_id'],
                                     title=self.title,
                                     text=self.text)


