import unittest
from zeroeighttrack import leaderboard_score

time = 20000


class ScoreCase(unittest.TestCase):

    def test_to_deciseconds(self):
        # given
        scale_params_list = [('perfect distance', 260, 20000), ('too short but in acceptance distance', 259, 20000),
                             ('too long but in acceptance distance', 261, 20000), ('too short distance', 250, 20869),
                             ('too long distance', 270, 19990)]

        for case, an_input, expected_result in scale_params_list:
            with self.subTest(msg="Checking to deciseconds() for time {} ".format(an_input)):
                print('testing for {} case with distance {}'.format(case, an_input))

                # when
                result = leaderboard_score.calculate_score(time, an_input)

                # then
                self.assertEqual(expected_result, result)

    def test_calculate_score_with_forgot_to_lap_penalty(self):
        print('testing for forgot to lap it case')

        # given
        expected_result = 20450

        # when
        result = leaderboard_score.calculate_score(time, 0)

        # then
        self.assertEqual(expected_result, result)
