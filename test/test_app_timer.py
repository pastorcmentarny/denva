from unittest import TestCase

from datetime import datetime
from datetime import timedelta

import app_timer


class Test(TestCase):

    def test_get_app_uptime_should_return_uptime(self):
        # given
        startup_time = datetime.now() + timedelta(days=-1,hours=-1,minutes=-2,seconds=-3)
        expected_result = 'App:1 d,1 h,2 m,3 s'

        # when
        result = app_timer.get_app_uptime(startup_time)

        # debug
        print(result)

        # then
        self.assertEqual(result, expected_result)

    def test_is_time_to_run_every_6_hours_should_return_true(self):
        # given
        seven_hours_ago = datetime.now() + timedelta(hours=-7,seconds=-1)

        # when
        result = app_timer.is_time_to_run_every_6_hours(seven_hours_ago)

        # then
        self.assertTrue(result)

    def test_is_time_to_run_every_6_hours_should_return_false(self):
        # given
        five_hours_ago = datetime.now() + timedelta(hours=-5,seconds=-1)

        # when
        result = app_timer.is_time_to_run_every_6_hours(five_hours_ago)

        # then
        self.assertFalse(result)