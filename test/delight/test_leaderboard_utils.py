from unittest import TestCase

from eighttrack import leaderboard_utils


class LeaderboardUtilsTest(TestCase):
    def test_to_deciseconds(self):
        # given
        scale_params_list = [('0', 0), ('0.1', 1), ('1', 10), ('1.0', 10), ('1.2.3', 623),
                             ('9.59.9', 5999), ('24.46.3', 14863), ('30.53.1', 18531)]

        for an_input, expected_result in scale_params_list:
            with self.subTest(msg="Checking to deciseconds() for time {} ".format(an_input)):
                # when
                result = leaderboard_utils.to_deciseconds(an_input)

                # debug
                print('for {} result is {} and expected result is {}'.format(an_input, result, expected_result))

                # then
                self.assertEqual(result, expected_result)
