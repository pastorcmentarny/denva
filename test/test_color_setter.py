import unittest

from overseer import color_setter


class MyTestCase(unittest.TestCase):
    def test_get__colour(self):
        # given
        color_params_list = [('red', ':255x0x0:'), ('garlic', 'rubbish'), ('blue', ':0x0x255:')]

        for an_input, expected_result in color_params_list:
            with self.subTest(msg="Checking to get_state_colour() for  {} ".format(an_input)):
                # when

                result = color_setter.get_color_for(an_input)

                # debug
                print('for {} result is {} and expected result is {}'.format(an_input, result, expected_result))

                # then
                self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
