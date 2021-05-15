import unittest

from denvapa import daily


# TODO convert to parameterized test
class DailyTestCases(unittest.TestCase):
    def test_get_now_and_next_event_should_return_last_from_previous_day_and_first_event_of_day_at_midnight(self):
        # given
        expected_result = ['23:00 - SLEEP', '06:30 - WAKE UP']

        # when
        result = daily.get_now_and_next_event(0)

        # then
        self.assertEqual(expected_result, result[0:2])

    def test_get_now_and_next_event_should_get_first_and_second_event(self):
        # given
        expected_result = ['06:30 - WAKE UP', '06:37 - 5 DEEP BREATH']

        # when
        result = daily.get_now_and_next_event(6 * 60 + 31)

        # then
        self.assertEqual(expected_result, result[0:2])

    def  test_get_now_and_next_event(self):
        # given
        expected_result = ['22:00 - RELAX', '22:25 - plan next day']

        # when
        result = daily.get_now_and_next_event(22 * 60 + 1)

        # then
        self.assertEqual(expected_result, result[0:2])

    def test_get_now_and_next_event_should_return_last_and_first_event_of_day(self):
        # given
        expected_result = ['23:00 - SLEEP', '06:30 - WAKE UP']

        # when
        result = daily.get_now_and_next_event(23 * 60 + 59)

        # then
        self.assertEqual(expected_result, result[0:2])
