import requests
import json
import os
import datetime

class WeatherForecast :
    history_of_weather = {}

    def __init__(self, latitude, longitude, date, rain):
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
        self.rain = rain

    def __setitem__(self, key, value):
        self.history_of_weather[key] = value

    def __getitem__(self,key):
        return self.history_of_weather[key]

    def __iter__(self):
        yield self.history_of_weather.items()


    def check_rain_forecast(self, data):
        if data[0] > 0.0:
            return 'Będzie padać'
        elif data[0] == 0.0:
            return 'Nie będzie padać'
        else:
            return 'Nie wiem'

    def items(self):
        for k, v in self.history_of_weather.items():
            yield k, v


f = 'history.txt'
if os.path.exists(f):
    with open(f,'r') as file:
        try:
            history_of_weather = json.load(file)
        except json.JSONDecodeError:
            history_of_weather = {}
else:
    history_of_weather = {}
tomorrow = datetime.date.today() + datetime.timedelta(days = 1)
formatted_tomorrow = tomorrow.strftime('%Y-%m-%d')
requested_date = input('Wpisz datę we formacie YYYY-mm-dd: ')

if requested_date == '' :
    requested_date = formatted_tomorrow

if requested_date in history_of_weather.keys():
    lat = history_of_weather[requested_date]['latitude']
    lon = history_of_weather[requested_date]['longitude']
    rai = history_of_weather[requested_date]['rain']
    weather = WeatherForecast(lat, lon, requested_date, rai)
    print(history_of_weather)
    print(f'Ta data ({requested_date}) była już sprawdzana')

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
        'daily' : 'rain_sum',
        'start_date' : requested_date,
        'end_date' : requested_date,
        'timezone' : 'auto'
    }

    url = requests.get('https://api.open-meteo.com/v1/forecast', params = params)
    rain = url.json()['daily']['rain_sum']
    weather = WeatherForecast(params['latitude'], params['longitude'], requested_date, rain)
    print(weather.check_rain_forecast(rain))
    history_of_weather[requested_date] = weather.__dict__
    with open(f, 'w') as file:
        json.dump(history_of_weather, file)
print('Te daty zostały już sprawdzone: ')
for requested_date in history_of_weather:
    print(requested_date)

