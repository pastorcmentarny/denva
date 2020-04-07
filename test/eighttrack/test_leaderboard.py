import unittest

from eighttrack import leaderboard

class LeaderboardTestCase(unittest.TestCase):
    def test_load_results(self):
        # given
        expected_first_result = {'date': '1.4', 'lap': 1, 'time': '24.46.3'}
        # when
        result = leaderboard.load_results()
        # then
        self.assertEqual(result[0],expected_first_result)
        self.assertEqual(len(result),6)


