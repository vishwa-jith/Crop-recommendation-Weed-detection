import requests
import pandas as pd
import numpy as np


def getWeather(district):
    response = requests.get(
        "http://api.weatherapi.com/v1/forecast.json?key=6e1498be712f43a081f200018203110&q="+district+"&days=10",).json()
    res = pd.DataFrame.from_records(response)
    forecast = res['forecastday':'name']
    f = pd.DataFrame.from_records(forecast['forecast']['forecastday'])
    weather = pd.DataFrame.from_records(f["day"])
    weather_input = [weather.avgtemp_c[0],
                     weather.avghumidity[0], 100*weather.totalprecip_mm[0]+100]
    return weather_input
