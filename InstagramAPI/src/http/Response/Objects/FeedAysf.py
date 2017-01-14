from InstagramAPI.src.http.Response.Objects.Suggestion import Suggestion


class FeedAysf(object):
    def __init__(self, data):
        self.landing_site_type = None
        self.uuid = None
        self.view_all_text = None
        self.feed_position = None
        self.landing_site_title = None
        self.is_dismissable = None
        self.suggestions = None
        self.should_refill = None
        self.display_new_unit = None
        self.fetch_user_details = None
        self.title = None

        self.landing_site_type = data['landing_site_type']
        self.uuid = data['uuid']
        self.view_all_text = data['view_all_text']
        self.feed_position = data['feed_position']
        self.landing_site_title = data['landing_site_title']
        self.is_dismissable = data['is_dismissable']
        suggestions = []
        if 'suggestions' in data and len(data['suggestions']):
            for suggestion in data['suggestions']:
                suggestions.append(Suggestion(suggestion))

        self.suggestions = suggestions
        self.should_refill = data['should_refill']
        self.display_new_unit = data['display_new_unit']
        self.fetch_user_details = data['fetch_user_details']
        self.title = data['title']

    def getLandingSiteType(self):
        return self.landing_site_type

    def getUuid(self):
        return self.uuid

    def getViewAllText(self):
        return self.view_all_text

    def getFeedPosition(self):
        return self.feed_position

    def getLandingSiteTitle(self):
        return self.landing_site_title

    def isDismissable(self):
        return self.is_dismissable

    def getSuggestions(self):
        return self.suggestions

    def shouldRefill(self):
        return self.should_refill

    def displayNewUnit(self):
        return self.display_new_unit

    def fetchUserDetails(self):
        return self.fetch_user_details

    def getTitle(self):
        return self.title
