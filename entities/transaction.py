from entities import Entity, IMGActivity


class Transaction(Entity):
    """
    Transaction
    """
    _query_table = 'TSTC'
    type = 'U'  # User transaction

    @property
    def text(self):
        text = self._get_text()

        if not text:
            self.type = 'C'  # Customizing transaction
            try:
                activity = IMGActivity(self._connection)
                activity.get(tcode=self.TCODE)
                text = activity.text
            except IndexError:
                return text

        return text