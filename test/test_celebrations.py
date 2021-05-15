import unittest
from unittest.mock import Mock

from common import dom_utils
from denvapa import celebrations


class CelebrationsTestCases(unittest.TestCase):
    def test_get_next_3_events(self):
        # when
        three_events_result = celebrations.get_next_3_events()

        # debug
        print(three_events_result)

        # then
        self.assertEqual(len(three_events_result), 3)
        for result in three_events_result:
            self.assertTrue(result)

    def test_get_today_with_event(self):
        # given
        timestamp_key = '0401'
        dom_utils.get_timestamp_key = Mock(return_value=timestamp_key)

        # when
        result = celebrations.get_today()

        # debug
        print(result)

        # then
        self.assertTrue(result)

    def test_get_today_without_event(self):
        # given
        timestamp_key = '0416'
        dom_utils.get_timestamp_key = Mock(return_value=timestamp_key)

        # when
        result = celebrations.get_today()

        # debug
        print(result)

        # then
        self.assertFalse(result)

    def test_get_sentence_from_list_of_events_with_2_events(self):
        # given
        events = ['event1', 'event2']

        # when
        result = celebrations.get_sentence_from_list_of_events(events)

        # debug
        print(result)

        # then
        self.assertEqual(result, 'event1 and event2')

    def test_get_sentence_from_list_of_events_with_3_events(self):
        # given
        events = ['event1', 'event2', 'event3']

        # when
        result = celebrations.get_sentence_from_list_of_events(events)

        # debug
        print(result)

        # then
        self.assertEqual(result, 'event1 event2 and event3')

    def test_day_left_text_get_today_for_zero(self):
        # given
        zero_days = 0

        # when
        result = celebrations.day_left_text(zero_days)

        # debug
        print(result)

        # then
        self.assertEqual(result, 'today')

    def test_day_left_text_get_tomorrow_for_one(self):
        # given
        one_day = 1

        # when
        result = celebrations.day_left_text(one_day)

        # debug
        print(result)

        # then
        self.assertEqual(result, 'tomorrow')

    def test_day_left_text_get_2_days_for_two(self):
        # given
        two_days = 2

        # when
        result = celebrations.day_left_text(two_days)

        # debug
        print(result)

        # then
        self.assertEqual(result, '2 days left')

    def test_day_left_text_get_5_days_for_five(self):
        # given
        five_days = 5

        # when
        result = celebrations.day_left_text(five_days)

        # debug
        print(result)

        # then
        self.assertEqual(result, '5 days left')

    def test_day_left_text_error_for_negative(self):
        # given
        negative_days = -1

        # when
        result = celebrations.day_left_text(negative_days)

        # debug
        print(result)

        # then
        self.assertEqual(result, 'error')
