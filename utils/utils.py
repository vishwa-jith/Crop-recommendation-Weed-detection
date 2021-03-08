import pickle
import time


def loadpickles(filename):
    with open(filename, 'rb') as f:
        model = pickle.load(f)
    return model


def getSeason():
    month = time.strftime("%m")
    seasons = {'Kharif     ': ['7', '8', '9', '10'],
               'Autumn     ': ['9', '10', '11'],
               'Summer     ': ['3', '4', '5', '6'],
               'Winter     ': ['12', '1', '2'],
               'Rabi       ': ['10', '11', '12', '1', '2', '3']}
    season = ""
    for key, value in seasons.items():
        for val in value:
            if(val == month):
                season = key
                break
    return season
