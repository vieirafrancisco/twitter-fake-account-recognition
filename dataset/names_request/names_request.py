import tweepy
import numpy as np
import pandas as pd
import time
import key

CONSUMER_KEY = key.CONSUMER_KEY
CONSUMER_SECRET = key.CONSUMER_SECRET

ACCESS_TOKEN = key.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = key.ACCESS_TOKEN_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

class GetNames:
    def __init__(self, origin_name, api):
        self.api = api
        self.names_list = []
        self.followers_list = []
        self.all_names = []
        self.get_users(origin_name)

    def get_names_size(self):
        return len(self.names_list)

    def get_names(self):
        return self.names_list

    def random(self, obj):
        index = np.random.randint(0, len(obj))
        return obj[index]

    def get_users(self, user_name):
        if(self.get_names_size() >= 1000):
            return
        try:
            print(self.get_names_size())
            user = api.get_user(user_name)

            # Verify if the number of tweets is more or iqual to 200
            if(user.statuses_count >= 200):
                if(user_name not in self.names_list):
                    self.names_list.append(user_name)

            self.followers_list = user.followers()
            for follower in self.followers_list:
                follower_name = follower.screen_name
                self.all_names.append(follower_name) # store all names
                if(follower.statuses_count >= 200):
                    if(follower_name not in self.names_list):
                        self.names_list.append(follower_name)
        except tweepy.RateLimitError:
            print("Rate time limite")
            for i in range(0, 15):
                time.sleep(60)
                print("Already passed " + str(i+1) + " minutes.")
        except tweepy.TweepError:
            print("Failed")
        except Exception as e:
            print(e)

        if(len(self.followers_list) == 0):
            self.get_users(self.random(self.all_names))
        else:
            self.get_users(self.random(self.followers_list).screen_name)

api = tweepy.API(auth)

names = GetNames('painGamingBR', api)
df = pd.DataFrame(names.get_names())
df.to_csv('csv/names2.csv')
