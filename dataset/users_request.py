from tweepy import RateLimitError, TweepError
import numpy as np
import time

# Users object list
users = []
# Screen names list
names = []

# User need have 200 or more posts and the language need to be portuguese
def add_data(user):
    if(user.statuses_count >= 200 and user.lang == 'pt' and user.screen_name not in names):
        users.append(user)
        names.append(user.screen_name)

# Random object
def random(obj):
    index = np.random.randint(0, len(obj))
    return obj[index]

def get_users(user):
    if(len(users) > 500):
        return
    try:
        # Append user object and screen name
        add_data(user)

        # Get followers from user
        followers = user.followers()

        # Append followers user object and screen name
        for follower in followers:
            add_data(follower)
    except RateLimitError:
        print(len(users))
        for i in range(15):
            time.sleep(60)
            print('In get_users function: Already passed ' + str(i+1) + ' minutes')
    except TweepError as e:
        print(e)
    except Exception as e:
        print(e)

    if(len(users) == 0):
        return
    else:
        # Recursion
        get_users(random(users))