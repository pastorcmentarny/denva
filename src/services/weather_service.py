import os
import logging
import data_files
import web_data
import app_timer
from datetime import datetime

weather_file = '../data/weather.txt'


def save_weather_to_file(weather_data: list):
    now = datetime.now()
    weather_data.append(str('{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second)))
    data_files.save_list_to_file(weather_data, weather_file)

    # load weather from file
    # if not exists, load from www
    # check when weather that was loaded from www is still new
    # if old then load from ww


def is_weather_data_expired(date: str) -> bool:
    last_check = date.split('-')
    return app_timer.is_time_to_run_every_6_hours(datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]),
                                                           int(last_check[3]), int(last_check[4]), int(last_check[5])))


def get_weather() -> list:
    print('Getting weather')
    if not os.path.exists(weather_file):
        print('File not exists. Getting weather from the web')
        weather_data = web_data.get_weather()
    else:
        print('loading data from the file')
        weather_data = data_files.load_weather(weather_file)
        if is_weather_data_expired(weather_data[len(weather_data) - 1]):
            print('weather in the file is out of date, Getting weather from the web')
            weather_data = web_data.get_weather()
        else:
            print('returning weather from the file')
            return weather_data
    if weather_data != ['Weather data N/A']:
        save_weather_to_file(weather_data)
        return weather_data
    print('Something went badly wrong')
    return ['Weather data N/A']


def test():
    test = ['Max temp.: 18 °C', 'Min temp.: 5 °C', 'Clear', 'Sunrise: 06:05', 'Sunset: 20:00',
            'UV: Moderate', 'Pollution: Moderate', 'Pollen: High']
    save_weather_to_file(test)
    weather = data_files.load_weather(weather_file)
    print(weather)
    last_check = weather[len(weather) - 1].split('-')
    print(app_timer.is_time_to_run_every_6_hours(datetime(int(last_check[0]), int(last_check[1]), int(last_check[2]),
                                                      int(last_check[3]), int(last_check[4]), int(last_check[5]))))
if __name__ == '__main__':
    print(get_weather())
