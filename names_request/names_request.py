import tweepy
import time
import numpy as np
import pandas as pd
import datetime as dt
import key

CONSUMER_KEY2 = key.CONSUMER_KEY2
CONSUMER_SECRET2 = key.CONSUMER_SECRET2

ACCESS_TOKEN2 = key.ACCESS_TOKEN2
ACCESS_TOKEN_SECRET2 = key.ACCESS_TOKEN_SECRET2

CONSUMER_KEY = key.CONSUMER_KEY
CONSUMER_SECRET = key.CONSUMER_SECRET

ACCESS_TOKEN = key.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = key.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

auth2 = tweepy.OAuthHandler(CONSUMER_KEY2, CONSUMER_SECRET2)
auth2.set_access_token(ACCESS_TOKEN2, ACCESS_TOKEN_SECRET2)

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
    if(len(user_list) >= 2000):
        return
    try:
        user = api.get_user(user_name)
        followers_list = user.followers()

        user_list.append(user.screen_name)
        info_list.append(user._json)

        for follower in followers_list:
            if(follower.screen_name not in user_list):
                user_list.append(follower.screen_name)
                info_list.append(follower._json)

        get_users(random(followers_list).screen_name, api)
    except:
        global time1, time2, api1, api2
        print("Time 1 " + str(time1) + " Time 2 " + str(time2))
        if(is_time(time1)):
            time1 = get_now_time()
            get_users(random(user.followers()).screen_name, api1)
        elif(is_time(time2)):
            time2 = get_now_time()
            get_users(random(user.followers()).screen_name, api2)
        else:
            print(len(user_list))
            for i in range(0, 15):
                time.sleep(60)
                print("Passed " + str(i+1) + " minute(s)")
            get_users(random(user.followers()).screen_name, api1)

api1 = tweepy.API(auth)
api2 = tweepy.API(auth2)

user_list = []
info_list = []
time1 = 0
time2 = 0
get_users('paiNGamingBR', api1)
print(len(user_list))

df_name = pd.DataFrame(user_list)
df_name.to_csv('csv/names2.csv')
df = pd.DataFrame(info_list)
df.to_csv('csv/info2.csv')
