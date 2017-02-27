from InstagramAPI.src.http.Response.Objects.Comment import Comment
from .Response import Response


class CommentResponse(Response):
    def __init__(self, response):
        self.comment = None

        if self.STATUS_OK == response['status']:
            if 'comment' in response and response['comment']:
                self.comments = Comment(response['comment'])

        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getComment(self):
        return self.comment
