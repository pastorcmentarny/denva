import unittest

from datetime import datetime

from common.gobshite_exception import GobshiteException
from denvapa import personal_stats

class PersonalStatsTests(unittest.TestCase):
    def test_convert_to_date_time_for_date(self):
        # given
        test_date = '2016-10-10'
        expected_result = datetime(2016,10,10)

        # when
        result = personal_stats.convert_to_date_time(test_date)

        # then
        self.assertEqual(expected_result,result)


    def test_convert_to_date_time_for_date_with_time(self):
        # given
        test_date = '2016-10-10-23-59'
        expected_result = datetime(2016,10,10,23,59)

        # when
        result = personal_stats.convert_to_date_time(test_date)

        # then
        self.assertEqual(expected_result,result)

        # when & then
        self.assertRaises(GobshiteException, personal_stats.convert_to_date_time, '2020-10-20-11-11-13')