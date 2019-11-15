from entities.entity import Entity
from entities.img_activity import IMGActivity


class Transaction(Entity):
    """
    Transaction
    """
    _query_table = 'TSTC'
    type = 'U'

    @property
    def text(self):
        text = self._get_text()

        if not text:
            self.type = 'C'
            try:
                activity = IMGActivity(self._connection)
                activity.get(tcode=self.TCODE)
                text = activity.text
            except IndexError:
                return text

        return text