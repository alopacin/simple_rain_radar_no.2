import requests
import json
import os
import datetime

class WeatherForecast :
    def __init__(self, latitude, longitude, date, temperature, windspeed):
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
        self.temperature = temperature
        self.windspeed = windspeed

    def __setitem__(self, key, value):
        pass

    def __getitem__(self, item):
        pass

    def __iter__(self):
        yield self


f = 'history.txt'
if os.path.exists(f):
    with open(f,'r') as file:
        try:
            history_of_weather = json.load(file)
        except json.JSONDecodeError:
            history_of_weather = {}
else:
    history_of_weather = {}
print(history_of_weather)
tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
formatted_tomorrow = tomorrow.strftime('%Y-%m-%d')
requested_date = input('Wpisz datę we formacie YYYY-mm-dd: ')

if requested_date == '' :
    requested_date = formatted_tomorrow

if requested_date in history_of_weather.keys():
    latitude = history_of_weather[requested_date]['latitude']
    longitude = history_of_weather[requested_date]['longitude']
    temperature = history_of_weather[requested_date]['temperature']
    windspeed = history_of_weather[requested_date]['windspeed']
    weather = WeatherForecast(latitude, longitude, requested_date, temperature, windspeed)
    print('ta data była juz sprawdzana')
    exit()

else:
    try:
        datetime.datetime.strptime(requested_date, '%Y-%m-%d')
    except ValueError:
        print('Nieprawidłowy format daty. Wprowadź datę we formacie YYYY-mm-dd lub zostaw puste'
              ' aby sprawdzić jutrzejszy dzień')
        exit()
    params = {
        'latitude' : '52',
        'longitude' : '16',
        'start_date' : requested_date,
        'end_date' : requested_date,
        'current_weather' : 'true',
    }
    url = requests.get('https://api.open-meteo.com/v1/forecast', params = params)

    get_temperature = url.json()['current_weather']['temperature']
    get_windspeed = url.json()['current_weather']['windspeed']
    weather = WeatherForecast(params['latitude'], params['longitude'], requested_date, get_temperature,get_windspeed)
    history_of_weather[requested_date] = weather.__dict__
    print(weather)
    print(history_of_weather)
    with open(f, 'w') as file:
        json.dump(history_of_weather, file)



