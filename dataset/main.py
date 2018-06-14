# MAIN
# author: Francisco, date: 27/02/2018

# Imports
from twitter_api import api, TweepError, RateLimitError
from measures import Measures
import pandas as pd
import time
import tweepy
import datetime

def is_empty(_list): # If the list is empty
    if(_list == []):
        return True
    else:
        return False

def get_timeline_user(screen_name):
    timeline = api.user_timeline(screen_name=screen_name, count=200)
    return timeline

def collectData(timeline):
    datetime_list = [] # The datetime list
    raw_hashtags = [] # The raw hashtags list
    date_list = [] # The raw date list

    for tweet in timeline:
        # Appending tweet's datetime with all atributes of date and time of each tweet
        datetime_list.append(datetime.datetime(
            year = tweet.created_at.year,
            month = tweet.created_at.month,
            day = tweet.created_at.day,
            hour = tweet.created_at.hour,
            minute = tweet.created_at.minute,
            second = tweet.created_at.second))

        # Collect the hashtags
        hashtags = tweet.entities['hashtags']
        if(not is_empty(hashtags)):
            raw_hashtags.append(hashtags[0]['text'])

        # Adding a tuple in a list with the date of the tweet
        date_list.append(datetime.date(
            year = tweet.created_at.year,
            month = tweet.created_at.month,
            day = tweet.created_at.day))

    return (datetime_list, date_list, raw_hashtags)

# Screen name list
screen_name_list = []

names_df = pd.read_csv("csv/names.csv", names = ['Screen_name']) # Data frame to screen names

for name in names_df['Screen_name']:
    screen_name_list.append(name)

# Instance of Measures object
rate = Measures()

_list = [] # List to store the datas in format of a dictionary

cont = 1
for screen_name in screen_name_list:
    # Final time list
    final_time_list = []

    # User caracteristics
    try:
        user = data.user(screen_name)
    except tweepy.RateLimitError:
        print("Rate Limit")
        for i in range(0, 15):
            time.sleep(60)
            print(str(i+1) + " minutes")
        user = data.user(screen_name)
    except tweepy.TweepError:
        print("Failed")
        continue

    # Get timeline
    try:
        timeline = get_timeline_user(screen_name)
    except tweepy.RateLimitError:
        print("Rate Limit")
        for i in range(0, 15):
            time.sleep(60)
            print(str(i+1) + " minutes")
        timeline = get_timeline_user(screen_name)
    except tweepy.TweepError:
        print("Failed")
        continue

    # The number of tweets in the user timeline
    number_tweets = len(timeline)
    print(number_tweets)
    print(screen_name)
    # Collect data from twitter and store in lists
    datetime_list, raw_date, hashtags = collectData(timeline)
    # Take the intervals of one tweet to another in seconds
    interval_list = rate.get_intervals(datetime_list)
    # Sort the interval list
    interval_list.sort()

    if(is_empty(interval_list)):
        print("Failed")
        continue

    # Take the thresholds of the interquartil range
    lim_sup, lim_inf = rate.limit_iqr(interval_list)
    # Creating another list without the outliers
    for value in interval_list:
        if(value <= lim_sup and value >= lim_inf): # If the value is inside of the limits
            final_time_list.append(value)

    # The day of week post of each tweet
    day_of_week_list = rate.day_of_week(raw_date)
    # Get the number of tweets in the particular week
    number_tweets_week = rate.get_number_tweets_week(day_of_week_list)

    if(number_tweets_week == 0): # To avoid division to 0
        number_tweets_week = 1

    # List of dataset information
    _list.append({
        'screen_name': screen_name,
        'id': user.id,
        'followers': user.followers_count,
        'friends': user.friends_count,
        'number_tweets': number_tweets,
        'number_interval_tweets': len(final_time_list),
        'mean_interval_tweets': '{:.2f}'.format(rate.mean(final_time_list)),
        'variance_interval_tweets': '{:.2f}'.format(rate.variance(final_time_list)),
        'standard_deviation_interval_tweets': '{:.2f}'.format(rate.standardDeviation(rate.variance(final_time_list))),
        'number_tweets_week': number_tweets_week,
        'monday_relative_frequence': day_of_week_list[0]/number_tweets_week,
        'tuesday_relative_frequence': day_of_week_list[1]/number_tweets_week,
        'wednesday_relative_frequence': day_of_week_list[2]/number_tweets_week,
        'thursday_relative_frequence': day_of_week_list[3]/number_tweets_week,
        'friday_relative_frequence': day_of_week_list[4]/number_tweets_week,
        'saturday_relative_frequence': day_of_week_list[5]/number_tweets_week,
        'sunday_relative_frequence': day_of_week_list[6]/number_tweets_week,
        'mean_day_week': '{:.2f}'.format(rate.mean(day_of_week_list)),
        'variance_day_week': '{:.2f}'.format(rate.variance(day_of_week_list)),
        'standard_deviation_day_week': '{:.2f}'.format(rate.standardDeviation(rate.variance(day_of_week_list))),
        'number_hashtags': len(rate.uniqueHashtag(hashtags)),
        'hashtag_per_tweet': len(rate.uniqueHashtag(hashtags))/number_tweets,
        'profile_image_url': str(user.profile_image_url),
        'profile_image_url_https': str(user.profile_image_url_https)
        })

    print("Success " + str(cont))
    cont += 1

# Save file
df = pd.DataFrame(_list)
df = df.get([
    'screen_name', 'id', 'followers', 'friends', 'number_tweets', 'number_interval_tweets', 'mean_interval_tweets',
    'variance_interval_tweets', 'standard_deviation_interval_tweets', 'number_tweets_week','monday_relative_frequence',
    'tuesday_relative_frequence', 'wednesday_relative_frequence', 'thursday_relative_frequence',
    'friday_relative_frequence', 'saturday_relative_frequence', 'sunday_relative_frequence', 'mean_day_week',
    'variance_day_week','standard_deviation_day_week','number_hashtags',
    'hashtag_per_tweet','profile_image_url','profile_image_url_https'
    ])
df.to_csv("csv/dataset.csv")
print("END")
