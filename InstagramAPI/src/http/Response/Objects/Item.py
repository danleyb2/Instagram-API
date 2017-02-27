from InstagramAPI.src.http.Response.Objects.Caption import Caption
from InstagramAPI.src.http.Response.Objects.Comment import Comment
from InstagramAPI.src.http.Response.Objects.Explore import Explore
from InstagramAPI.src.http.Response.Objects.HdProfilePicUrlInfo import HdProfilePicUrlInfo
from InstagramAPI.src.http.Response.Objects.User import User
from InstagramAPI.src.http.Response.Objects.Usertag import Usertag
from InstagramAPI.src.http.Response.Objects.VideoVersions import VideoVersions


class Item(object):
    PHOTO = 1
    VIDEO = 2

    def __init__(self, item):

        self.taken_at = None
        self.pk = None
        self.id = None
        self.device_timestamp = None
        self.media_type = None
        self.code = None
        self.client_cache_key = None
        self.filter_type = None
        self.image_versions2 = None
        self.original_width = None
        self.original_height = None
        self.view_count = 0
        self.organic_tracking_token = None
        self.has_more_comments = None
        self.max_num_visible_preview_comments = None
        self.comments = None
        self.comment_count = 0
        self.caption = None
        self.caption_is_edited = None
        self.photo_of_you = None
        self.video_versions = None
        self.has_audio = False
        self.video_duration = ''
        self.user = None
        self.likers = ''
        self.like_count = 0
        self.preview = ''
        self.has_liked = False
        self.explore_context = ''
        self.explore_source_token = ''
        self.explore = ''
        self.impression_token = ''
        self.usertags = None

        self.taken_at = item['taken_at']
        self.pk = item['pk']
        self.id = item['id']
        self.device_timestamp = item['device_timestamp']
        self.media_type = item['media_type']
        self.code = item['code']
        self.client_cache_key = item['client_cache_key']
        self.filter_type = item['filter_type']
        images = []
        if 'image_versions2' in item \
                and 'candidates' in item['image_versions2'] \
                and len(item['image_versions2']['candidates']):

            for image in item['image_versions2']['candidates']:
                images.append(HdProfilePicUrlInfo(image))

        self.image_versions2 = images
        self.original_width = item['original_width']
        self.original_height = item['original_height']
        if 'view_count' in item and item['view_count']:
            self.view_count = item['view_count']

        self.organic_tracking_token = item['organic_tracking_token']
        if 'has_more_comments' in item:
            self.has_more_comments = item['has_more_comments']
        if 'max_num_visible_preview_comments' in item:
            self.max_num_visible_preview_comments = item['max_num_visible_preview_comments']
        comments = []
        if 'comments' in item and len(item['comments']):
            for comment in item['comments']:
                comments.append(Comment(comment))

        self.comments = comments
        if 'comment_count' in item:
            self.comment_count = item['comment_count']
        if item['caption']:
            self.caption = Caption(item['caption'])
        self.caption_is_edited = item['caption_is_edited']
        self.photo_of_you = item['photo_of_you']
        if 'video_versions' in item and item['video_versions']:
            videos = []
            for video in item['video_versions']:
                videos.append(VideoVersions(video))
            self.video_versions = videos

        if 'has_audio' in item and item['has_audio']:
            self.has_audio = item['has_audio']

        if 'video_duration' in item and item['video_duration']:
            self.video_duration = item['video_duration']
        self.user = User(item['user'])
        likers = []
        if 'likers' in item and len(item['likers']):
            for liker in item['likers']:
                likers.append(User(liker))
        self.likers = likers
        if 'like_count' in item and item['like_count']:
            self.like_count = item['like_count']
        if 'preview' in item and item['preview']:
            self.preview = item['preview']
        if 'has_liked' in item and item['has_liked']:
            self.has_liked = item['has_liked']
        if 'explore_context' in item and item['explore_context']:
            self.explore_context = item['explore_context']
        if 'explore_source_token' in item and item['explore_source_token']:
            self.explore_source_token = item['explore_source_token']
        if 'explore' in item and item['explore']:
            self.explore = Explore(item['explore'])
        if 'impression_token' in item and item['impression_token']:
            self.impression_token = item['impression_token']
        if 'usertags' in item and item['usertags']:
            self.usertags = Usertag(item['usertags'])

    def getTakenAt(self):
        return self.taken_at

    def getUsernameId(self):
        return self.user.getUsernameId()

    def getMediaId(self):
        return self.id

    def getDeviceTimestamp(self):
        return self.device_timestamp

    def isVideo(self):
        return self.media_type == self.VIDEO

    def isPhoto(self):
        return self.media_type == self.PHOTO

    def getCode(self):
        return self.code

    def getClientCacheKey(self):
        return self.client_cache_key

    def getFilterType(self):
        return self.filter_type

    def getImageVersions(self):
        return self.image_versions2

    def getOriginalWidth(self):
        return self.original_width

    def getOriginalHeight(self):
        return self.original_height

    def getViewCount(self):
        return self.view_count

    def getOrganicTrackingToken(self):
        return self.organic_tracking_token

    def hasMoreComments(self):
        return self.has_more_comments

    def getMaxNumVisiblePreviewComments(self):
        return self.max_num_visible_preview_comments

    def getComments(self):
        return self.comments

    def getCommentCount(self):
        return self.comment_count

    def getCaption(self):
        return self.caption

    def isCaptionEdited(self):
        return self.caption_is_edited

    def isPhotoOfYou(self):
        return self.photo_of_you

    def getVideoVersions(self):
        return self.video_versions

    def hasAudio(self):
        return self.has_audio

    def getVideoDuration(self):
        return self.video_duration

    def getUser(self):
        return self.user

    def getMediaLikers(self):
        return self.likers

    def getLikeCount(self):
        return self.like_count

    def getPreview(self):
        return self.preview

    def hasLiked(self):
        return self.has_liked

    def getExploreContext(self):
        return self.explore_context

    def getExploreSourceToken(self):
        return self.explore_source_token

    def getExplore(self):
        return self.explore

    def getImpressionToken(self):
        return self.impression_token

    def getUsertags(self):
        return self.usertags

    def getlikers(self):
        return self.likers

    def getPk(self):
        return self.pk
