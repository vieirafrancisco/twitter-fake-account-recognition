# author: Francisco, date: 27/02/2018

import os
import sys

import pandas as pd
import numpy as np
import tweepy
import yaml

from timeline import user_timeline, number_hashtags, number_tweets_with_hashtags
from measures import get_intervals, days_of_week, tweets_in_week


def get_twitter_api():
    keys = yaml.dump(yaml.load("api_key.yaml"))

    consumer_key = keys["CONSUMER_KEY"]
    consumer_secret = keys["CONSUMER_SECRET"]

    access_token = keys["ACCESS_TOKEN"]
    access_token_secret = keys["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    if(not api):
        raise Exception("Error in twitter API!")
        sys.exit(-1)

    return api


def load_dataset(path):
    df = pd.read_csv(path)
    if "Unnamed: 0" in df.columns:
        df = df.drop(["Unnamed: 0"], axis=1)
    return df


def generate_activity_dataset(path, count=200, result_file_name="activity_dataset"):
    users = load_dataset(path)
    api = get_twitter_api()

    instance = {}

    for user in users:
        try:
            timeline = api.user_timeline(id=user.id, count=count)
        except tweepy.TweepError as e:
            print(e)
            continue
        except Exception as e:
            print(e)
            continue

        save_instance(get_instance(user, timeline), result_file_name)
        print(f"User: {user.id} ==> {user.screen_name}, OK!")


def save_instance(instance, file_name):
    if file_name not in os.listdir("resultset/"):
        df = pd.DataFrame([instance.values()], columns=instance.keys())
    else:
        df = pd.read_csv("resultset/"+file_name)
        new_instance_df = pd.DataFrame([instance.values()], columns=instance.keys())
        df = df.append(new_instance_df, ignore_index=True, sort=False)

    df.to_csv("resultset/"+file_name, index=False)


def get_instance(user, timeline):

    instance = {}

    instance['screen_name'] = user['screen_name']
    instance['id'] = user['id']
    instance['followers'] = user['followers']
    instance['friends'] = user['friends']
    instance['number_tweets'] = number_tweets = len(timeline)
    intervals = get_tweet_intervals()
    instance['inter_mean'] = np.mean(intervals)
    instance['inter_std'] = np.std(intervals, ddop=1)
    count_week_day = get_count_week_day()
    instance['0'] = count_week_day[0]/sum(count_week_day)
    instance['1'] = count_week_day[1]/sum(count_week_day)
    instance['2'] = count_week_day[2]/sum(count_week_day)
    instance['3'] = count_week_day[3]/sum(count_week_day)
    instance['4'] = count_week_day[4]/sum(count_week_day)
    instance['5'] = count_week_day[5]/sum(count_week_day)
    instance['6'] = count_week_day[6]/sum(count_week_day)
    instance['abs_mean_week_days'] = np.mean(count_week_day)
    instance['abs_std_week_days'] = np.std(count_week_day, ddop=1)
    hashtags_count = get_hashtags_count()
    instance['hashtags_count'] = hashtags_count
    instance['hashtag_per_tweet'] = hashtags_count/get_count_tweets_with_hashtags()

    return instance


def get_tweet_intervals():
    pass

