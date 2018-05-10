# Twitter fake account detection
## Description:
The idea is to detect and classificate fake accounts in social media (in special Twitter) to provide eficiente data and well caracterized, to people who need a good material to study data analysis or who wants work with the data to some future project.
## Dataset atributes:
    'screen_name': 	                        User screen name
    'id':                                   User id
    'followers':                            Number of followers
    'friends':                              Number of friends
    'number_tweets':                        Number of tweets analized
    'number_interval_tweets':               Number of intervals from one tweet to another
    'mean_interval_tweets':                 Mean of tweet's intervals
    'variance_interval_tweets':             Variance of tweet's intervals
    'standard_deviation_interval_tweets':   Standard deviation of tweet's intervals
    'number_tweets_week':                   Total number of tweets in all week days
    'monday_relative_frequence':            Monday relative frequence
    'tuesday_relative_frequence':           Tuesday relative frequence
    'wednesday_relative_frequence':	        Wednesday relative frequence
    'thursday_relative_frequence':          Thursday relative frequence
    'friday_relative_frequence':            Friday relative frequence
    'saturday_relative_frequence':          Saturday relative frequence
    'sunday_relative_frequence':            Sunday relative frequence
    'mean_day_week':                        Mean of week day
    'variance_day_week':                    Variance of week day
    'standard_deviation_day_week':          Standard deviation of week day
    'number_hashtags':                      Total number of hashtags in the number of tweets
    'hashtag_per_tweet':                    Number of hashtags divided by the number of tweets
    'profile_image_url':                    The profile image URL
    'profile_image_url_https':              The profile image URL in https

_Obs: The attributes based in tweets it's relative to 200 tweets in the user's timeline, but some accounts don't have this amount of tweets, that is the result will be less than this quantity_
