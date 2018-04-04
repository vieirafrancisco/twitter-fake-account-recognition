# MAIN
# author: Francisco, date: 27/02/2018

# Imports
from auth import Auth
from measures import Measures
import pandas as pd

def collectTimeFromTwitter(screen_name):
    timeline = data.timeline(screen_name, 200)

    raw_time = [] # The raw time list

    for tweet in timeline:
        # Adding a tuple in a list with the time divided
        raw_time.append((tweet.created_at.hour,
                         tweet.created_at.minute,
                         tweet.created_at.second))

    raw_time.reverse()
    return raw_time

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

for index in range(0, len(screen_name_list)):
    # Final time list
    final_time_list = []
    # Screen name
    screen_name = screen_name_list[index]
    # Collect data from twitter and store in a list
    collected_data = collectTimeFromTwitter(screen_name)
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

    ## CREATING A FILE TO STORE THE USER DATAS ##
    _list.append({'Screen_name': screen_name,
                  'Length': len(final_time_list),
                  'Mean': '{:.2f}'.format(rate.mean(final_time_list)),
                  'Variance': '{:.2f}'.format(rate.variance(final_time_list)),
                  'Standard_Deviation': '{:.2f}'.format(rate.standardDeviation(rate.variance(final_time_list)))})

    print("Sucesso", index, "!")

# Save file
df = pd.DataFrame(_list)
print(df)
# df.to_html("csv/dataset.csv")
print("FIM")
