import numpy as np

def days_of_week(dates):
    week_list = [0,0,0,0,0,0,0]
    for date in dates:
        week_list[date] += 1

    return week_list

def tweets_in_week(values):
    number_tweets = 0
    for value in values:
        number_tweets += value
    return number_tweets

# Get the intevals from one tweet to another
def get_intervals(datetimes):
    interval_list = []
    for i in range(len(datetimes)-1, 0, -1):
        interval = datetimes[i] - datetimes[i - 1]
        interval = interval.total_seconds()
        interval_list.append(abs(interval))
    print('IW:', str(len(interval_list)))
    # Get the limits of the values from interquartil range
    lim_sup, lim_inf = limit_iqr(interval_list)
    # List of intervals without the outliers
    intervals = eliminate_outliers((lim_sup, lim_inf), interval_list)
    return intervals

# Return the interquartil range limits
def limit_iqr(values):
    quartile_1, quartile_3 = np.percentile(values, [25, 75])
    iqr = quartile_3 - quartile_1
    lim_sup = quartile_3 + (iqr * 1.5)
    lim_inf = quartile_1 - (iqr * 1.5)
    return lim_sup, lim_inf

# Eliminate the outliers of a list of values
def eliminate_outliers(limites, values):
    without_outliers = []
    lim_sup, lim_inf = limites
    for value in values:
        if(value <= lim_sup and value >= lim_inf):
            without_outliers.append(value)
    return without_outliers