from InstagramAPI.src.http.Response.Objects.Comment import Comment
from Response import Response


class CommentResponse(Response):
    def __init__(self, response):
        self.comments = None
        self.has_more_comments = None
        self.next_max_id = None

        if self.STATUS_OK == response['status']:
            self.next_max_id = response['next_max_id']
            comments = []
            for comment in response['comments']:
                comments.append(Comment(comment))
            self.comments = comments

        else:
            self.setMessage(response['message'])
        self.setStatus(response['status'])

    def getComments(self):
        return self.comments

    def getNextMaxId(self):
        return self.next_max_id

    def has_more_comments(self):
        return self.has_more_comments
