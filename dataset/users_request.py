from tweepy import RateLimitError, TweepError
import numpy as np
import time

# Users object list
users = []

# Able
def is_able(user):
    if(user.statuses_count >= 200 and user.lang == 'pt'):
        return True
    else:
        return False

# Random object
def random(obj):
    index = np.random.randint(0, len(obj))
    return obj[index]

def get_users(user):
    if(len(users) > 5):
        return
    try:
        # Append user object
        if(is_able(user) and user not in users):
            users.append(user)

        # Get followers from user
        followers = user.followers()

        # Append followers user object
        for follower in followers:
            if(is_able(follower) and follower not in users):
                users.append(follower)
    except RateLimitError:
        for i in range(15):
            time.sleep(60)
            print('Already passed ' + str(i+1) + ' minutes')
    except TweepError as e:
        print(e)

    if(len(users) == 0):
        return
    else:
        # Recursion
        get_users(random(users))