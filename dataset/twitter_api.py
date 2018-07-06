# Librarys
from tweepy import API, Cursor, OAuthHandler, TweepError, RateLimitError
from key import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import sys

consumer_key = CONSUMER_KEY
consumer_secret = CONSUMER_SECRET

access_token = ACCESS_TOKEN
access_token_secret = ACCESS_TOKEN_SECRET

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# API class instance
api = API(auth)

if(not api):
    print('Cant Authenticate')
    sys.exit(-1)