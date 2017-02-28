from .Objects.Suggestion import Suggestion
from .Response import Response


class AddressBookResponse(Response):
    def __init__(self):
        self._types = {}
        self._types["items"] = [Suggestion]
        self.items = None
