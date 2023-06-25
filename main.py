import requests
import json
import os

f = 'history.txt'
if os.path.exists(f):
    with open(f,'r') as file:
        try:
            history_of_weather = json.load(file)
        except json.JSONDecodeError:
            history_of_weather = {}

class WeatherForecast :
    def __init__(self, latitude, longitude, start_date, end_date, temperature, windspeed):
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.temperature = temperature
        self.windspeed = windspeed

    def __setitem__(self, key, value):
        self.key = value

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass

#inquiry = input('Wpisz datę we formacie YY-mm-dd: ')
params = {
    'latitude' : '52',
    'longitude' : '16',
    'start_date' : '2023-06-25',
    'end_date' : '2023-06-25',
    'current_weather' : 'true',
}
url = requests.get('https://api.open-meteo.com/v1/forecast', params = params)

get_temperature = url.json()['current_weather']['temperature']
get_windspeed = url.json()['current_weather']['windspeed']
print(url.json())
weather = WeatherForecast(
    latitude=params['latitude'],
    longitude = params['longitude'],
    start_date = params['start_date'],
    end_date = params['end_date'],
    temperature = get_temperature,
    windspeed = get_windspeed
    )
print(weather)

with open(f, 'w') as file:
    json.dump(weather.__dict__, file)
print(url.status_code)