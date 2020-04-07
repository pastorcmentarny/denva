import unittest

from eighttrack import leaderboard


class LeaderboardTestCase(unittest.TestCase):
    def test_load_results(self):
        # given
        expected_first_result = {'date': '1.4', 'lap': 1, 'time': '24.46.3', 'id': 3}
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
