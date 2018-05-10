import numpy as np
import calendar

class Measures():

    def uniqueHashtag(self, hts):
        return np.unique(hts)
        
    def day_of_week(self, dates):
        week_list = [0,0,0,0,0,0,0]
        for date in dates:
            week_list[date.weekday()] += 1

        return week_list

    def get_intervals(self, datetimes):
        interval_list = []
        for i in range(1, len(datetimes)):
            interval = datetimes[i] - datetimes[i - 1]
            interval_list.append(abs(interval.total_seconds()))
        return interval_list

    def limit_iqr(self, values):
        try:
            quartile_1, quartile_3 = np.percentile(values, [25, 75])
        except Exception as e:
            print("Error in iqr function: " + str(e))
            pass
        iqr = quartile_3 - quartile_1
        lim_sup = quartile_3 + (iqr * 1.5)
        lim_inf = quartile_1 - (iqr * 1.5)
        return lim_sup, lim_inf

    def mean(self, _list):
        return np.mean(_list)

    def variance(self, _list):
        return np.var(_list)

    def standardDeviation(self, var): # Variance in argument
        return np.sqrt(var)

    def get_number_tweets_week(self, _list):
        number_tweets = 0

        for tweets_day in _list:
            number_tweets += tweets_day

        return number_tweets
