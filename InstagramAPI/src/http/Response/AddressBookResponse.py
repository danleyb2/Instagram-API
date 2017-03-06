from InstagramAPI.src.http.Response.Objects.Suggestion import Suggestion
from InstagramAPI.src.http.Response.Response import Response


class AddressBookResponse(Response):
    def __init__(self):
        self._types = {}

        self._types["items"] = [Suggestion]
        self.items = None
