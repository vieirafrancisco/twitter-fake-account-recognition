# MAIN
# author: Francisco, date: 27/02/2018

# Imports
from twitter_api import api
from timeline import user_timeline, get_datetimes, get_dates, number_hashtags, number_tweets_with_hashtags
from measures import get_intervals, days_of_week, tweets_in_week
from users_request import get_users, users
import pandas as pd
import numpy as np

# Console output data
def console_output(screen_name, intervals):
    print('Screen_name: ' + str(screen_name) + ' Number intervals: ' + str(intervals))

# Number of statuses
NUMBER_STATUSES = 200

# List to store the datas in format of a dictionary
_list = [] 

# Fisrt user screen name
screen_name = 'brunoneyo'
# First user
first_user = api.get_user(screen_name=screen_name)
# Get users
get_users(first_user)

for user in users:
    # Screen name
    screen_name = user.screen_name
    # Timeline
    timeline = user_timeline(screen_name)
    # In case of error returns 0
    if(timeline == 0):
        continue

    # Intervals of one tweet to another
    intervals = get_intervals(get_datetimes(timeline))
    # Days of week
    week_day = days_of_week(get_dates(timeline))
    # Number of tweets
    number_tweets = tweets_in_week(week_day)
    # Number of hashtags
    hashtags = number_hashtags(timeline) 
    # Number tweets with hashtags
    tweets_with_hashtags = number_tweets_with_hashtags(timeline)
    if(tweets_with_hashtags == 0):
        tweets_with_hashtags = 1

    # List of dataset information
    _list.append({
        'screen_name': screen_name,
        'id': user.id,
        'followers': user.followers_count,
        'friends': user.friends_count,
        'number_tweets': 200,
        'number_interval_tweets': len(intervals),
        'mean_interval_tweets': '{:.2f}'.format(np.mean(intervals)),
        'variance_interval_tweets': '{:.2f}'.format(np.var(intervals)),
        'standard_deviation_interval_tweets': '{:.2f}'.format(np.sqrt(np.var(intervals))),
        'number_tweets_week': number_tweets,
        'monday_relative_frequence': week_day[0]/number_tweets,
        'tuesday_relative_frequence':week_day[1]/number_tweets,
        'wednesday_relative_frequence': week_day[2]/number_tweets,
        'thursday_relative_frequence': week_day[3]/number_tweets,
        'friday_relative_frequence': week_day[4]/number_tweets,
        'saturday_relative_frequence': week_day[5]/number_tweets,
        'sunday_relative_frequence': week_day[6]/number_tweets,
        'mean_day_week': '{:.2f}'.format(np.mean(week_day)),
        'variance_day_week': '{:.2f}'.format(np.var(week_day)),
        'standard_deviation_day_week': '{:.2f}'.format(np.sqrt(np.var(week_day))),
        'number_hashtags': hashtags,
        'hashtag_per_tweet': '{:.2f}'.format(hashtags/tweets_with_hashtags),
        'profile_image_url': str(user.profile_image_url),
        'profile_image_url_https': str(user.profile_image_url_https)
        })
    
    console_output(screen_name, len(intervals))

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
df.to_csv("csv/dataset_false.csv")
print("END")
