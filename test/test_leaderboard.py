import unittest

import config_test
from zeroeighttrack import leaderboard


class LeaderboardTestCase(unittest.TestCase):
    def test_load_results(self):
        # given
        expected_first_result = config_test.result_as_dict
        # when
        result = leaderboard.load_results()
        # then
        self.assertEqual(result[0], expected_first_result)
        self.assertEqual(len(leaderboard.results), len(result))

    def test_should_get_result_by_id(self):
        # given
        result_id = 6
        expected_result = {
            'date': '7.4.2020',
            'time': '25.21.9',
            'time_in_ds': 15219,
            'lap': 1,
            'id': result_id
        }
        # when
        result = leaderboard.get_result_by_id(result_id)

        # then
        self.assertEqual(expected_result, result)

    def test_should_return_None_if_id_do_not_match_when_get_result_by_id(self):
        # given
        result_id = 999
        # when
        result = leaderboard.get_result_by_id(result_id)

        # then
        self.assertEqual(result, {})

    def test_should_add_result(self):
        # given
        id = len(leaderboard.results) + 1
        lap_result = '59.59.9--1.1.2068--1'
        expected_result = config_test.get_result_with_id(id, 1)

        # when
        result = leaderboard.add_result(lap_result)

        # then
        self.assertEqual(leaderboard.get_result_by_id(id), expected_result)
        leaderboard.remove_result_by_id(id)

    def test_should_remove_result(self):
        # given
        id = len(leaderboard.results) + 1
        lap_result = '59.59.9--1.1.2068--9'
        expected_result = config_test.get_result_with_id(id, 9)

        result_id = leaderboard.add_result(lap_result)
        self.assertEqual(leaderboard.get_result_by_id(result_id), expected_result)

        # when
        leaderboard.remove_result_by_id(id)

        # then
        self.assertEqual(len(leaderboard.results), id - 1)
