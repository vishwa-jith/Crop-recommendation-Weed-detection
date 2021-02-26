import requests
import pandas as pd


def getWeather(district):
    response = requests.get(
        "http://api.weatherapi.com/v1/forecast.json?key=6e1498be712f43a081f200018203110&q="+district+"&days=10",).json()
    res = pd.DataFrame.from_records(response)
    forecast = res['forecastday':'name']
    f = pd.DataFrame.from_records(forecast['forecast']['forecastday'])
    return {"temperature": f.avgtemp_c, "humidity": f.avghumidity, "rainfall": f.totalprecip_mm}
