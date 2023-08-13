import requests
import datetime
import json
import os

# utworzenie klasy wraz z metodami
class WeatherForecast:
    def __init__(self, filename="history.txt"):
        self.filename = filename
        self.history_of_raining = self.load_history()

    def __setitem__(self, date, rain_data):
        self.history_of_raining[date] = rain_data

    def __getitem__(self, date):
        return self.history_of_raining[date]

    def __iter__(self):
        for date in self.history_of_raining:
            yield date

    def items(self):
        for date, rain_data in self.history_of_raining.items():
            yield date, rain_data

    def load_history(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_history(self):
        with open(self.filename, 'w') as file:
            json.dump(self.history_of_raining, file)

    def get_forecast(self, date, latitude="51.51", longitude="-0.13"):
        response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&"
                                f"hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}"
                                f"&end_date={date}")
        rain = response.json()['daily']['rain_sum']
        self[date] = rain
        self.save_history()
        return rain

    @staticmethod
    def check_rain_forecast(data):
        if data[0] > 0.0:
            return 'Będzie padać'
        elif data[0] == 0.0:
            return 'Nie będzie padać'
        else:
            return 'Nie wiem'

# sprawdzenie czy plik istnieje
f = 'history.txt'
if os.path.exists(f):
    with open(f,'r') as file:
        try:
            history_of_weather = json.load(file)
        except json.JSONDecodeError:
            history_of_weather = {}

# glowny kod programu
weather_forecast = WeatherForecast()

requested_date = input('Podaj we formacie YYYY-mm-dd jaką datę chcesz sprawdzić: ')
if not requested_date:
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    requested_date = tomorrow.strftime('%Y-%m-%d')

if requested_date in weather_forecast:
    print(weather_forecast.check_rain_forecast(weather_forecast[requested_date]))
    print("Ta data już została sprawdzona.")
else:
    rain_data = weather_forecast.get_forecast(requested_date)
    print(weather_forecast.check_rain_forecast(rain_data))

# wyswietlenie wszystkich sprawdzonych dat
print('Daty dla których znana jest pogoda:')
for date in weather_forecast:
    print(date)
