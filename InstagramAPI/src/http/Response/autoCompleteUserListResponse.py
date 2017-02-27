from .Response import Response


class autoCompleteUserListResponse(Response):
    def __init__(self):
        self.expires = None
        self.users = None
