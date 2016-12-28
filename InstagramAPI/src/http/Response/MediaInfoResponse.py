from Comment import Comment
from Response import Response
from User import User


class MediaInfoResponse(Response):
    def __init__(self, response):

        self.taken_at = None
        self.image_url = None
        self.like_count = None
        self.likers = None
        self.comments = None

        if self.STATUS_OK == response['status']:

            self.taken_at = response['items'][0]['taken_at']
            self.image_url = response['items'][0]['image_versions2']['candidates']['0'][
                'url']  # FIXME list indices must be integers, not str
            self.like_count = response['items'][0]['like_count']
            likers = []

            for liker in response['items'][0]['likers']:
                likers.append(User(liker))

            self.likers = likers
            comments = []

            for comment in response['items'][0]['comments']:
                comments.append(Comment(comment))

            self.comments = comments

        else:
            self.setMessage(response['message'])

        self.setStatus(response['status'])
        self.setFullResponse(response)

    def getTakenTime(self):
        return self.taken_at

    def getImageUrl(self):
        return self.image_url

    def getLikeCount(self):
        return self.like_count

    def getLikers(self):
        return self.likers

    def getComments(self):
        return self.comments
