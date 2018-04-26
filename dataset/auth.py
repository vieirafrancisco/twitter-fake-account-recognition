# Librarys
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from authorization import key

consumer_key = key.CONSUMER_KEY
consumer_secret = key.CONSUMER_SECRET

access_token = key.ACCESS_TOKEN
access_token_secret = key.ACCESS_TOKEN_SECRET

# Twitter authorization class
class Auth():

    def __init__(self):
        # Authorization
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)

        # API object
        self.api = API(self.auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)

    def timeline(self, screen_name, count):
        return self.api.user_timeline(screen_name = screen_name, count = count)

    def user(self, screen_name):
        return self.api.get_user(screen_name = screen_name)
