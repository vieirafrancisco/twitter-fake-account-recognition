from twitter_api import api, Cursor, TweepError, RateLimitError
import datetime
import calendar
import time

# Number of tweets from analysis
NUMBER_TWEETS = 200

# Return a user timeline
def user_timeline(screen_name):
    try:
        #timeline = Cursor(api.user_timeline, screen_name=screen_name).items(NUMBER_TWEETS)
        # Try to iterate with the timeline (if don't, get a exception)
        #timeline.page_iterator.next()
        timeline = api.user_timeline(screen_name=screen_name, count=NUMBER_TWEETS)
    except RateLimitError:
        for i in range(15):
            time.sleep(60)
            print('In user_timeline function: Already passed ' + str(i+1) + ' minutes')
        #timeline = Cursor(api.user_timeline, screen_name=screen_name).items(NUMBER_TWEETS)
        timeline = api.user_timeline(screen_name=screen_name, count=NUMBER_TWEETS)
    except TweepError as e:
        if(e.args[0] == 'Twitter error response: status code = 401'):
            print('Not authorized access in this user timeline: status code = 401')
        else:
            print(e)
        return 0
    return timeline

# Return a list of tweets
def get_tweets(timeline):
    tweets = []
    for tweet in timeline:
        tweets.append(tweet.text)
    return tweets
    
# Return a datetime list
def get_datetimes(timeline):
    datetimes = []
    for tweet in timeline:
        date = tweet.created_at
        datetimes.append(datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=date.hour,
            minute=date.minute,
            second=date.second
        ))
    return datetimes

# Return a date list
def get_dates(timeline):
    dates = []
    for tweet in timeline:
        date = tweet.created_at
        dates.append(calendar.weekday(
            year=date.year,
            month=date.month,
            day=date.day
        ))
    return dates

# Number of hashtags
def number_hashtags(timeline):
    number_hashtags = 0
    for tweet in timeline:
        hashtags = tweet.entities['hashtags']
        if(hashtags != []):
            number_hashtags += len(hashtags)
    return number_hashtags

# Number of tweets with hashtags
def number_tweets_with_hashtags(timeline):
    number_tweets = 0
    for tweet in timeline:
        hashtags = tweet.entities['hashtags']
        if(hashtags != []):
            number_tweets += 1
    return number_tweets