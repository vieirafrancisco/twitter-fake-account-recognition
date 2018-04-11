# MAIN
# author: Francisco, date: 27/02/2018

# Imports
from auth import Auth
from measures import Measures
import pandas as pd

NUMBER_TWEETS = 200

def isEmpty(_list): # If the list is empty
    if(_list == []):
        return True
    else:
        return False

def get_timeline_user(screen_name):
    timeline = data.timeline(screen_name, NUMBER_TWEETS)
    return timeline

def collectData(timeline):
    raw_time = [] # The raw time list
    raw_hashtags = [] # The raw hashtags list
    date_list = [] # The raw date list

    for tweet in timeline:
        # Adding a tuple in a list with the time divided
        raw_time.append((tweet.created_at.hour,
                         tweet.created_at.minute,
                         tweet.created_at.second))

        # Collect the hashtags
        hashtags = tweet.entities['hashtags']
        if(not isEmpty(hashtags)):
            raw_hashtags.append(hashtags[0]['text'])

        # Adding a tuple in a list with the date of the tweet
        date_list.append((tweet.created_at.year,
                          tweet.created_at.month,
                          tweet.created_at.day))

    raw_time.reverse() # Reverse the list
    return (raw_time, date_list, raw_hashtags)

# Screen name list
screen_name_list = []

names_df = pd.read_csv("csv/teste2.csv", names = ['Screen_name']) # Data frame to screen names

for name in names_df['Screen_name']:
    screen_name_list.append(name)

# Instance of Measures object
rate = Measures()
# Instance of Auth object
data = Auth()

_list = [] # List to store the datas in format of a dictionary

for screen_name in screen_name_list:
    # User caracteristics
    user = data.user(screen_name)
    # Final time list
    final_time_list = []

    # Get timeline
    timeline = get_timeline_user(screen_name)

    # Collect data from twitter and store in lists
    collected_data, raw_date, hashtags = collectData(timeline)

    # Turn the date in seconds
    seconds = rate.turnIntoSeconds(collected_data)
    # Take the interval of the time of each tweet
    interval = rate.getIntervals(seconds)
    # Sort the interval list
    interval.sort()
    # Take the thresholds of the interquartil range
    upper_threshold, lower_threshold = rate.limitToOutliers(interval)
    # Creating another list without the outliers
    for value in interval:
        if(value <= upper_threshold and value >= lower_threshold): # If the value is inside of the limits
            final_time_list.append(value)


    # The day of week post of each tweet
    day_of_week_list = rate.dayOfTheWeek(raw_date)
    # Get the number of tweets in the particular week
    number_tweets_week = rate.getNumberTweetsWeek(day_of_week_list)
    if(number_tweets_week == 0):
        number_tweets_week = 1


    ## CREATING A FILE TO STORE THE USER DATAS ##
    _list.append({'screen_name': screen_name,
                  'id': user.id,
                  'followers': user.followers_count,
                  'friends': user.friends_count,
                  'number_tweets': len(final_time_list),
                  'mean': '{:.2f}'.format(rate.mean(final_time_list)),
                  'variance': '{:.2f}'.format(rate.variance(final_time_list)),
                  'standard_deviation': '{:.2f}'.format(rate.standardDeviation(rate.variance(final_time_list))),
                  'monday': day_of_week_list[0]/number_tweets_week,
                  'tuesday': day_of_week_list[1]/number_tweets_week,
                  'wednesday': day_of_week_list[2]/number_tweets_week,
                  'thursday': day_of_week_list[3]/number_tweets_week,
                  'friday': day_of_week_list[4]/number_tweets_week,
                  'saturday': day_of_week_list[5]/number_tweets_week,
                  'sunday': day_of_week_list[6]/number_tweets_week,
                  'mean_day_week': '{:.2f}'.format(rate.mean(day_of_week_list)),
                  'variance_day_week': '{:.2f}'.format(rate.variance(day_of_week_list)),
                  'standard_deviation_day_week': '{:.2f}'.format(rate.standardDeviation(rate.variance(day_of_week_list))),
                  'number_hashtags': len(rate.uniqueHashtag(hashtags)),
                  'hashtag_per_tweet': rate.hashtagPerTweet(hashtags, NUMBER_TWEETS)})

    print("Success")

# Save file
df = pd.DataFrame(_list)
df = df.get(['screen_name', 'id', 'followers', 'friends', 'number_tweets', 'mean', 'variance', 'standard_deviation',
             'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'mean_day_week', 'variance_day_week',
             'standard_deviation_day_week', 'number_hashtags', 'hashtag_per_tweet'])
print(df)
df.to_csv("csv/dataset.csv")
print("END")
