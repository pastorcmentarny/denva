import os
import logging
import data_files
import web_data

weather_file = '../data/weather.json'


def save_weather_to_fire(weather_data: list):
    data_files.save_list_to_file(weather_data, weather_file)

    # load weather from file
    # if not exists, load from www
    # check when weather that was loaded from www is still new
    # if old then load from ww


def is_weather_up_to_date(weather_data):
    pass


def get_weather() -> list:
    print('')
    if not os.path.exists(weather_file):
        weather_data = web_data.get_weather()
    else:
        weather_data = data_files.load_weather()
        if is_weather_up_to_date(weather_data):
            return weather_data
        else:
            weather_data = web_data.get_weather()
    if weather_data != ['Weather data N/A']:
        save_weather_to_fire(weather_data)
        return weather_data
    return ['Weather data N/A']
