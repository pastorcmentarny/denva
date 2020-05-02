from datetime import datetime
from datetime import timedelta
from unittest import TestCase

from common import app_timer


class Test(TestCase):

    def test_get_app_uptime_should_return_uptime(self):
        # given
        startup_time = datetime.now() + timedelta(days=-1, hours=-1, minutes=-2, seconds=-3)
        expected_result = 'App:1 d,1 h,2 m,3 s'

        # when
        result = app_timer.get_app_uptime(startup_time)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_is_time_to_run_every_6_hours_should_return_true(self):
        # given
        seven_hours_ago = datetime.now() + timedelta(hours=-7, seconds=-1)

        # when
        result = app_timer.is_time_to_run_every_6_hours(seven_hours_ago)

        # then
        self.assertTrue(result)

    def test_is_time_to_run_every_6_hours_should_return_false(self):
        # given
        five_hours_ago = datetime.now() + timedelta(hours=-5, seconds=-1)

        # when
        result = app_timer.is_time_to_run_every_6_hours(five_hours_ago)

        # then
        self.assertFalse(result)

    def test_is_time_to_run_every_hour_is_true(self):
        # given
        four_hours_ago = datetime.now() + timedelta(hours=-4, seconds=-1)

        result = app_timer.is_time_to_run_every_hour(four_hours_ago)

        # then
        self.assertTrue(result)

    def test_is_time_to_run_every_hour_is_false(self):
        # given
        few_seconds_ago = datetime.now() + timedelta(seconds=-10)

        result = app_timer.is_time_to_run_every_hour(few_seconds_ago)

        # then
        self.assertFalse(result)

    def test_is_time_to_run_every_5_minutes_is_true(self):
        # given
        three_hours_ago = datetime.now() + timedelta(hours=-3, seconds=-1)

        result = app_timer.is_time_to_run_every_5_minutes(three_hours_ago)

        # then
        self.assertTrue(result)

    def test_is_time_to_run_every_5_minutes_is_false(self):
        # given
        few_seconds_ago = datetime.now() + timedelta(seconds=-9)

        result = app_timer.is_time_to_run_every_5_minutes(few_seconds_ago)

        # then
        self.assertFalse(result)

    def test_is_time_to_send_email(self):
        # given
        two_hours_ago = datetime.now() + timedelta(hours=-2, seconds=-1)

        result = app_timer.is_time_to_send_email(two_hours_ago)

        # then
        self.assertTrue(result)

    def test_is_time_to_send_report_email(self):
        # given
        seven_hours_ago = datetime.now() + timedelta(hours=-7, seconds=-1)

        # when
        result = app_timer.is_time_to_send_report_email(seven_hours_ago)

        # then
        self.assertTrue(result)


