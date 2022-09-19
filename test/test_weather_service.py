import unittest
from datetime import datetime

from services import weather_service


class WeatherServiceTestCases(unittest.TestCase):
    def test_is_weather_data_is_not_expired_for_current_time(self):
        # given
        now = datetime.now()
        weather_timestamp = str(
            '{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))

        # when
        result = weather_service.__is_weather_data_expired(weather_timestamp)

        # then
        self.assertFalse(result)

    def test_is_weather_data_is_expired_for_old_date(self):
        # given
        now = datetime(2020, 1, 2, 3, 4, 5)
        weather_timestamp = str(
            '{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))

        # when
        result = weather_service.__is_weather_data_expired(weather_timestamp)

        # then
        self.assertTrue(result)

    def test_something(self):
        # given
        now = datetime.now()
        weather_timestamp = str(
            '{}-{}-{}-{}-{}-{}'.format(now.year, now.month, now.day, now.hour, now.minute, now.second))

        # when
        result = weather_service.__is_weather_data_expired(weather_timestamp)

        # then
        self.assertFalse(result)

    def test_cleanup_weather_data(self):
        # given
        weather = """Today.
Maximum daytime temperature: 18 degrees Celsius;
Minimum nighttime temperature: 5 degrees Celsius.
Clear.
Sunrise: 06:05; Sunset: 20:00.
UV: Moderate;
Pollution: Moderate;
Pollen: High."""
        expected_result = ['Max temp.: 18 °C', 'Min temp.: 5 °C', 'Clear', 'Sunrise: 06:05', 'Sunset: 20:00',
                           'UV: Moderate', 'Pollution: Moderate', 'Pollen: High']

        # when
        result = weather_service.__cleanup_weather_data(weather)

        # then
        self.assertEqual(expected_result, result)
