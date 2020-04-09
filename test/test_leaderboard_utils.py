from unittest import TestCase

from eighttrack import leaderboard_utils
import gobshite_exception
import config_test


class Test(TestCase):
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
                self.assertEqual(expected_result, result)

    def test_is_invalid_time(self):
        # given
        params_list = [(None, False), ('', False), (' ', False), ('time', False), ('1,2', False), ('1.2.3.4', False),
                       ('60.0', False), ('0.61.3', False), ('1.F', False), ('-0', False), ('-0.1', False),
                       ('-1.0', False),
                       ('-1.2.3', False), ('0', True), ('0.1', True), ('1.0', True), ('1.2.3', True)]
        for an_input, expected_result in params_list:
            with self.subTest(msg="Checking to deciseconds() for time {} ".format(an_input)):
                # when
                result = leaderboard_utils.is_valid_time(an_input)

                # debug
                print('for "{}" result is {} and expected result is {}'.format(an_input, result, expected_result))

                # then
                self.assertEqual(expected_result, result)

    # tag-test-exception
    def test_to_deciseconds_should_throw_exception_for_invalid_time(self):
        # when & then
        self.assertRaises(gobshite_exception.GobshiteException, leaderboard_utils.to_deciseconds, '')

    def test_convert_lap_result_request_to_dict(self):
        # given
        lap_result_from_request = '24.46.2--2.2.2002--1'
        expected_result = config_test.result_as_dict

        # when
        result = leaderboard_utils.convert_lap_result_request_to_dict(lap_result_from_request, 7)

        # then
        self.assertEqual(result, expected_result)

    def test_convert_result_to_line(self):
        # given
        lap = config_test.result_as_dict
        expected_result = config_test.result_as_line_in_file
        # when
        result = leaderboard_utils.convert_result_to_line(lap)

        self.assertEqual(expected_result, result)

    def test_convert_results_to_list_of_string(self):
        # given
        lap = config_test.result_as_dict
        laps_list = [lap, lap]

        expected_result = [config_test.result_as_line_in_file, config_test.result_as_line_in_file]
        # when
        result = leaderboard_utils.convert_results_to_list_of_string(laps_list)

        # then
        self.assertEqual(expected_result, result)

    def test_convert_line_to_result(self):
        # given
        expected_result = config_test.result_as_dict
        line = config_test.result_as_line_in_file

        # when
        result = leaderboard_utils.convert_line_to_result(line)

        # then
        self.assertEqual(expected_result, result)
