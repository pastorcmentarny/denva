import unittest

import config_test
from zeroeighttrack import leaderboard

EMPTY_LIST = []


class LeaderboardTestCase(unittest.TestCase):
    def test_load_results(self):
        # given
        expected_first_result = config_test.result_as_dict
        # when
        result = leaderboard.load_results()
        # then
        self.assertEqual(result[2], expected_first_result)
        self.assertEqual(len(leaderboard.results), len(result))

    def test_should_get_result_by_id(self):
        # given
        result_id = 7
        expected_result = {
            'date': '7.4.2020',
            'time': '25.21.9',
            'time_in_ds': 15219,
            'lap': 1,
            'id': result_id,
            'distance': 0
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
        new_id = len(leaderboard.results) + 1

        expected_result = config_test.get_result_with_id(new_id, 1)

        # when
        result = leaderboard.add_result(config_test.last_result_as_request)

        # then
        self.assertEqual(leaderboard.get_result_by_id(new_id), expected_result)

        leaderboard.remove_result_by_id(new_id)

        self.assertEqual(EMPTY_LIST, leaderboard.get_position_for_id(new_id))

    def test_should_remove_result(self):
        # given
        id = len(leaderboard.results) + 1

        expected_result = config_test.get_result_with_id(id, 1)

        result_id = leaderboard.add_result(config_test.last_result_as_request)
        self.assertEqual(leaderboard.get_result_by_id(result_id), expected_result)

        # when
        leaderboard.remove_result_by_id(id)

        # then
        self.assertEqual(len(leaderboard.results), id - 1)

    def test_get_position_for_id(self):
        # when
        result = leaderboard.get_position_for_id(4)
        self.assertEqual(1, result)
