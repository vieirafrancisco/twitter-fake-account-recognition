import numpy as np

class Measures():

    def turnIntoSeconds(self, times):
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.seconds_list = []

        for time in times:
            self.hour = time[0] * 3600 # Turn hour in seconds
            self.minute = time[1] * 60 # Turn minute in seconds
            self.second = time[2]

            self.seconds_list.append(self.hour + self.minute + self.second)

        return self.seconds_list

    def getIntervals(self, values):
        self.interval_list = []
        for i in range(0, len(values) - 1):
            self.interval_list.append(values[i + 1] - values[i])

        return self.interval_list

    def limitToOutliers(self, values):
        self.quartile_1, self.quartile_3 = np.percentile(values, [25, 75])
        self.iqr = self.quartile_3 - self.quartile_1
        self.lim_sup = self.quartile_3 + (self.iqr * 1.5)
        self.lim_inf = self.quartile_1 - (self.iqr * 1.5)
        return self.lim_sup, self.lim_inf

    def mean(self, _list):
        return np.mean(_list)

    def variance(self, _list):
        return np.var(_list)

    def standardDeviation(self, var): # Variance in argument
        return np.sqrt(var)
