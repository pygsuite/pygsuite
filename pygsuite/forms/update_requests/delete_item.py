from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class DeleteItemRequest(object):
    def __init__(self, location: int):
        self.location = location

    @property
    def request(self):
        return {"deleteItem": {
            "location": {'index': self.location},
        }}
