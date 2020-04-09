import unittest

from eighttrack import leaderboard


class LeaderboardTestCase(unittest.TestCase):
    def test_load_results(self):
        # given
        expected_first_result = {'date': '1.4', 'id': 3, 'lap': 1, 'time': '24.46.3', 'time_in_ds': 14863}
        # when
        result = leaderboard.load_results()
        # then
        self.assertEqual(result[0], expected_first_result)
        self.assertEqual(len(result), 6)

    def test_should_get_result_by_id(self):
        # given
        result_id = 6
        expected_result = {
            'date': '7.4',
            'time': '25.21.9',
            'time_in_ds': 15219,
            'lap': 1,
            'id': result_id
        }
        # when
        result = leaderboard.get_result_by_id(result_id)

        # then
        self.assertEqual(result, expected_result)

    def test_should_return_None_if_id_do_not_match_when_get_result_by_id(self):
        # given
        result_id = 999
        # when
        result = leaderboard.get_result_by_id(result_id)

        # then
        self.assertEqual(result, {})

    def test_should_add_result(self):
        # given
        id = 7
        lap_result = '59.59.9--1.1--1'
        expected_result = {
            'date': '1.1',
            'time': '59.59.9',
            'time_in_ds': 35999,
            'lap': 1,
            'id': id
        }

        # when
        result = leaderboard.add_result(lap_result)

        # then
        self.assertEqual(result, id)
        self.assertEqual(leaderboard.get_result_by_id(id), expected_result)
