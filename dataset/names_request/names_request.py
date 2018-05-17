import tweepy
import time
import numpy as np
import pandas as pd
import datetime as dt
import key

CONSUMER_KEY = key.CONSUMER_KEY
CONSUMER_SECRET = key.CONSUMER_SECRET

ACCESS_TOKEN = key.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = key.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

def get_now_time():
    now_time = dt.timedelta(hours = dt.datetime.now().hour,
                            minutes = dt.datetime.now().minute,
                            seconds = dt.datetime.now().second).total_seconds()
    return now_time

def is_time(time):
    now_time = get_now_time()
    if(time == 0 or abs(time - now_time) >= 850):
        return True
    else:
        return False

def random(obj):
    index = np.random.randint(0, len(obj))
    return obj[index]

def get_users(user_name, api):
    if(len(user_list) >= 1000):
        return

    try:
        user = api.get_user(user_name)
        timeline = user.timeline(count = 200)
        print(len(user_list))

        if(len(timeline) >= 200):
            global followers_list
            followers_list = user.followers()

            user_list.append(user.screen_name)
            info_list.append(user._json)

            for follower in followers_list:
                if(follower.screen_name not in user_list):
                    user_list.append(follower.screen_name)
                    info_list.append(follower._json)
    except tweepy.RateLimitError:
        print("Number of names:", len(user_list))
        for i in range(0, 15):
            time.sleep(60)
            print("Already passed " + str(i+1) + " minute(s)")
    except tweepy.TweepError as e:
        print(e)

    get_users(random(followers_list).screen_name, api)

api = tweepy.API(auth)

user_list = []
info_list = []
followers_list = []
time1 = 0
time2 = 0
get_users('brunoneyo', api)
print(len(user_list))

df_name = pd.DataFrame(user_list)
df_name.to_csv('csv/names.csv')
df = pd.DataFrame(info_list)
df.to_csv('csv/info.csv')
