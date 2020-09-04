import unittest
from unittest.mock import Mock

from common import dom_utils
from denvapa import celebrations


class CelebrationsTests(unittest.TestCase):
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
