from twitter_api import api, Cursor, TweepError, RateLimitError
import datetime
import calendar
import time

# Number of tweets from analysis
NUMBER_STATUSES = 200

# Get timeline with cursor
def get_timeline(screen_name):
    timeline = []
    values = Cursor(api.user_timeline, screen_name=screen_name).items(NUMBER_STATUSES)
    for tweet in values:
        timeline.append(tweet)
    return timeline

# Wait 15 minutes
def waiting_time():
    for i in range(15):
        time.sleep(60)
        print('Already passed ' + str(i+1) + ' minutes')

# Return a user timeline
def user_timeline(screen_name):
    try:
        timeline = get_timeline(screen_name)
    except TweepError as e:
        # String of the exception message
        msg = e.args[0]
        # Rate time limit: status code = 429
        if(msg == 'Twitter error response: status code = 429'):
            waiting_time()
            timeline = get_timeline(screen_name)
            return timeline
        # Not authorized: status code = 401
        elif(msg == 'Twitter error response: status code = 401'):
            print('Not authorized')
        else:
            print(e)
        return 0
    except Exception as e:
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