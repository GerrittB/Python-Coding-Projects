# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.
        
        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.
        Args:
            city: city name (str)
            year: the year to get the data for (int)
        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_d_info(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).
        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)
        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model
    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial
    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    
    output = []
    for d in degs:
    	output.append(pylab.polyfit(x, y, d))
    #returns pylab arrays
    return output 
    pass


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model
    Returns:
        a float for the R-squared error term
    """
    
    mse = (estimated-y)@(estimated-y)
    mean = pylab.mean(y)
    var = (y-mean) @(y-mean)
    #calculates and returns R^2 error term
    r_2 = 1 - mse/var

    return r_2
    pass

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.
    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.
    Returns:
        None
    """
    for model in models:
    	fit = pylab.polyfit(x, y, model)
    	predictor = pylab.poly1d(fit)
    	predictions = predictor(x)
    	pylab.scatter(x, y, color = 'b')
    	pylab.plot(x, predictions, 'r')
    	
    	if model ==1:
    		pylab.title("Degree: "+str(model)+ ", $R^{2}$ : " + str(r_squared(y, predictions)) + "\n" + str(se_over_slope(x ,y ,predictions, fit)))
    		pylab.show()
    	else:
    		pylab.title("Degree: "+str(model)+ ", $R^{2}$ : " + str(r_squared(y, predictions)))

    	pylab.show()
    pass

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.
    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)
    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    #calculates avg annual temperature for multiple cities
    avg_year_data = []
    for year in years: 
    	year_info = []
    	for city in multi_cities:
    		year_info.append(pylab.mean(climate.get_yearly_temp(city, year)))
    	avg_year_data.append(sum(year_info)/len(year_info))
    #returns pylab 1-d array of floats
    return pylab.array(avg_year_data)
    pass

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.
    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average
    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    #calculates moving average of y
    avg = []
    for i in range (len(y)):
        if i ==0:
            avg.append(y[0])
        elif i < window_length:
            avg.append(pylab.mean(y[0:i+1]))
        else: 
            avg.append(pylab.mean(y[i-window_length+1:i+1]))
    #returns pylab 1-d array with same length as y
    return avg
    

def rmse(y, estimated):
    """
    Calculate the root mean square error term.
    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model
    Returns:
        a float for the root mean square error term
    """
    #computes and returns root mean square error term
    mse = (estimated-y)@(estimated-y)
    mean = mse/len(y)
    return mean**0.5
    pass

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 
    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)
    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    #calculates the standard deviation of averaged yearly temp for multi_cities
    stds = []
    for year in years:
        d365_info = pylab.zeros(365)
        d366_info = pylab.zeros(366)
        
        for city in multi_cities:
            if len(climate.get_yearly_temp(city, year)) == 365:
                d365_info += climate.get_yearly_temp(city, year)
            else:
                d366_info += climate.get_yearly_temp(city, year)
        if pylab.sum(d365_info) > pylab.sum(d366_info):
            d_info = d365_info
        else:
            d_info = d366_info

        d_info = d_info/len(multi_cities)
        mean = pylab.mean(d_info)
        
        variance = 0
        for value in d_info:
            variance += (value - mean)*(value - mean)
        stds.append(pylab.sqrt(variance/len(d_info)))
    return pylab.array(stds)
    pass

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.
    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.
    Returns:
        None
    """
    #calculates RMSE and plots test data
    for model in models:
    	predictor = pylab.poly1d(model)
    	predictions = predictor(x)
    	pylab.scatter(x, y, color = 'b')
    	pylab.plot(x, predictions, 'r')
    	pylab.title("Degree: "+str(len(model)-1)+ ", $RMSE$ : " + str(rmse(y, predictions)))

    	pylab.show()
    pass

if __name__ == '__main__':

    pass 

    # Part A.4
    c = Climate("data.csv")
    day_data = []
    year_data = []
    years = []

    for i in range(1961,2010):
    	years.append(i)
    	day_data.append(c.get_d_info("NEW YORK", 1, 10, i))
    	year_data.append(c.get_yearly_temp("NEW YORK", i))

   	## Problem 4:I
    evaluate_models_on_training(pylab.array(years), pylab.array(day_data), [1])
	
	## Problem 4:II
    year_averages = [] 
    for year in year_data:
    	year_averages.append(pylab.mean(year))
    evaluate_models_on_training(pylab.array(years), pylab.array(year_averages), [1])

    # Part B
    cities_avg = gen_cities_avg(c, CITIES, [i for i in range (1961, 2010)])
    evaluate_models_on_training(pylab.array(years), pylab.array(cities_avg), [1])

    # Part C
    cities_moving_avg = moving_average(cities_avg, 5)
    evaluate_models_on_training(pylab.array(years), (cities_moving_avg), [1])

    # Part D.2
    fit_1 = pylab.polyfit(pylab.array(years), cities_moving_avg, 1)
    fit_2 = pylab.polyfit(pylab.array(years), cities_moving_avg, 2)
    fit_20 = pylab.polyfit(pylab.array(years), cities_moving_avg, 20)

    test_years = [i for i in range (2010, 2016)]
    test_cities_avg = gen_cities_avg(c, CITIES, [i for i in range (2010, 2016)])
    evaluate_models_on_testing(pylab.array(test_years), test_cities_avg, [fit_1, fit_2, fit_20])

    # Part E
    cities_stds = gen_std_devs(c, CITIES, [i for i in range (1961, 2010)])
    cities_stds_movavg = moving_average(cities_stds, 5)
    evaluate_models_on_training(pylab.array(years), cities_stds_movavg, [1])