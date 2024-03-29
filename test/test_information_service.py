from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from gateways import web_data_gateway
from services import information_service, weather_service


class InformationServiceTestCases(TestCase):
    def test_get_data_about_rickmansworth(self):
        # given
        crime_data = "Crime data N/A"  # FIXME currently data is not provided due to COVID-19
        flood_data = "Flooding. 0 severe flooding warnings that are danger to life, 0 flooding warnings that require immediate action, 0 flooding alerts that flooding is possible."
        weather_data = [
            "Maximum daytime temperature: 19 degrees Celsius",
            "Minimum nighttime temperature: 8 degrees Celsius",
            "Sunny intervals changing to cloudy by nighttime",
            "Sunrise: 06:03",
            "Sunset: 20:02",
            "UV: Moderate",
            "Pollution: Low",
            "Pollen: High"
        ]
        o2_data = "None of the cell sites close to your location currently has any reported outages."
        web_data_gateway.get_crime = Mock(return_value=crime_data)
        web_data_gateway.get_flood = Mock(return_value=flood_data)
        weather_service.get_weather = Mock(return_value=weather_data)
        web_data_gateway.get_o2_status = Mock(return_value=o2_data)

        expected_result = {

            "crimes": "Crime data N/A",
            "floods": "Flooding. 0 severe flooding warnings that are danger to life, 0 flooding warnings that require immediate action, 0 flooding alerts that flooding is possible.",
            "o2": "None of the cell sites close to your location currently has any reported outages.",
            "weather": [
                "Maximum daytime temperature: 19 degrees Celsius",
                "Minimum nighttime temperature: 8 degrees Celsius",
                "Sunny intervals changing to cloudy by nighttime",
                "Sunrise: 06:03",
                "Sunset: 20:02",
                "UV: Moderate",
                "Pollution: Low",
                "Pollen: High"
            ]
        }

        # when
        result = information_service.get_data_about_rickmansworth()
        result.pop('date')  # date is not part of the test
        # then
        self.assertEqual(expected_result, result)

    def test_is_rickmansworth_data_expired_is_true(self):
        # given
        expired_date = '2019-12-19'

        # when
        result = information_service.is_rickmansworth_data_expired(expired_date)

        # then
        self.assertTrue(result)

    def test_is_rickmansworth_data_expired_if_date_is_missing(self):
        # given
        expired_date = ''

        # when
        result = information_service.is_rickmansworth_data_expired(expired_date)

        # then
        self.assertTrue(result)

    def test_is_rickmansworth_data_expired_if_date_is_with_time(self):
        # given
        expired_date = '2019-12-19-10-11-12'

        # when
        result = information_service.is_rickmansworth_data_expired(expired_date)

        # then
        self.assertTrue(result)

    def test_is_rickmansworth_data_expired_is_false_for_valid_data(self):
        # given
        today = datetime.now()
        today_date_as_text = f'{today.year}-{today.month}-{today.day}'

        # when
        result = information_service.is_rickmansworth_data_expired(today_date_as_text)

        # debug
        print(result)

        # then
        self.assertFalse(result)
