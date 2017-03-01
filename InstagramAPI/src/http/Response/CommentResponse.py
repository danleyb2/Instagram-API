from InstagramAPI.src.http.Response.Objects.Comment import Comment
from .Response import Response


class CommentResponse(Response):
    def __init__(self):
        self.comment = None # FIXME shouldn't this be a Comment instance?
