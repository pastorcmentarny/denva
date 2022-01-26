from unittest import TestCase

import config
from services import networkcheck_service as networkcheck

PERFECT = 'Perfect'
GOOD = 'Good'
POOR = 'POOR'


class NetworkCheckTestCases(TestCase):
    def test_network_check_should_return_perfect(self):
        if config.run_slow_test():
            # given
            expected_result = {'status': 'Perfect', 'result': '6 of 6 pages were loaded', 'problems': []}

            # when
            result = networkcheck.network_check(False)

            # then
            self.assertEqual(expected_result, result)

            # debug
            print(result)
        else:
            self.skipTest('running fast test only. test_network_check_should_return_perfect skipped.')

    def test__get_network_status_should_return_perfect_for_all_url_works(self):
        result = networkcheck._get_network_status(6)
        self.assertEqual(result, PERFECT)

    def test__get_network_status_should_return_good_for_5_url_works(self):
        result = networkcheck._get_network_status(5)
        self.assertEqual(result, GOOD)

    def test__get_network_status_should_return_good_for_4_url_works(self):
        result = networkcheck._get_network_status(4)
        self.assertEqual(result, GOOD)

    def test__get_network_status_should_return_poor_for_3_url_works(self):
        result = networkcheck._get_network_status(3)
        self.assertEqual(result, POOR)

    def test__get_network_status_should_return_poor_for_2_url_works(self):
        result = networkcheck._get_network_status(2)
        self.assertEqual(result, POOR)

    def test__get_network_status_should_return_down_for_1_url_works(self):
        result = networkcheck._get_network_status(1)
        self.assertEqual(result, 'DOWN?')

    def test__get_network_status_should_return_down_for_0_url_works(self):
        result = networkcheck._get_network_status(0)
        self.assertEqual(result, 'DOWN!')
