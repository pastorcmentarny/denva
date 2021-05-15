import unittest
from datetime import datetime
from unittest.mock import Mock

from common import dom_utils
from reports import report_service


class ReportServiceTestCases(unittest.TestCase):
    def test_get_last_two_days_report_difference_should_return_error_if_report_is_missing(self):
        # given
        expected_result = 'Unable to generate difference between because at least one of the report do not exists.' \
                          'Reports:2 days ago: False. Yesterday: False'
        two_days_ago = datetime(2020, 1, 1)
        one_day_ago = datetime(2020, 1, 2)
        dom_utils.get_two_days_ago_date = Mock(return_value=two_days_ago)
        dom_utils.get_yesterday_date = Mock(return_value=one_day_ago)

        # when
        result = report_service.get_last_two_days_report_difference()

        # then
        if 'error' not in result:
            self.fail('no error key in result but it should be ')
        else:
            error_message = result['error']

            # debug
            print(error_message)

            # then
            self.assertEqual(expected_result, result['error'])
