import unittest

from common import status
from delight import delight_utils


class MyTestCase(unittest.TestCase):

    def test_get_state_colour(self):
        # given
        scale_params_list = [(0, (255, 0, 0)), (1, (255, 224, 32)), (2, (0, 255, 0))]

        for an_input, expected_result in scale_params_list:
            with self.subTest(msg="Checking to get_state_colour() for  {} ".format(an_input)):
                # when
                an_status = status.Status(an_input)
                result = delight_utils.get_state_colour(an_status)

                # debug
                print('for {} result is {} and expected result is {}'.format(an_input, result, expected_result))

                # then
                self.assertEqual(expected_result, result)
