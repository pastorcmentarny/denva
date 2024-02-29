import unittest

from common import get_description_for


class GetDescriptionForTestCases(unittest.TestCase):

    def test_iqa_from_tvoc_for_radioactive_air(self):
        # given
        tvoc = '128256'
        expected_result = {
            'score': 'BAD',
            'value': int(tvoc),
            'action': 'Use only if unavoidable!',
            'information': 'Unacceptable Air Quality! Use only if unavoidable and only for short periods.'
        }

        # when
        result = get_description_for.iqa_from_tvoc(tvoc)

        # then
        self.assertEqual(expected_result, result)

    def test_iqa_from_tvoc_for_clean_air(self):
        # given
        tvoc = '50'
        expected_result = {
            'score': 'Very Good',
            'value': int(tvoc),
            'action': 'No action required',
            'information': 'Clean air'
        }

        # when
        result = get_description_for.iqa_from_tvoc(tvoc)

        # then
        self.assertEqual(expected_result, result)

    def test_iqa_from_tvoc_for_good_air(self):
        # given
        tvoc = '250'
        expected_result = {
            'score': 'Good',
            'value': int(tvoc),
            'action': 'Ventilation recommended.',
            'information': 'Good Air Quality'
        }

        # when
        result = get_description_for.iqa_from_tvoc(tvoc)

        # then
        self.assertEqual(expected_result, result)

    def test_iqa_from_tvoc_for_medium_air(self):
        # given
        tvoc = '750'
        expected_result = {
            'score': 'Medium',
            'value': int(tvoc),
            'action': 'Ventilation required.',
            'information': 'Air Quality is not good. (Not recommended for exposure for than year)'
        }

        # when
        result = get_description_for.iqa_from_tvoc(tvoc)

        # then
        self.assertEqual(expected_result, result)

    def test_iqa_from_tvoc_for_poor_air(self):
        # given
        tvoc = '3500'
        expected_result = {
            'score': 'POOR',
            'value': int(tvoc),
            'action': 'Ventilate now!',
            'information': 'Air Quality is POOR. (Not recommended for exposure for than month)'
        }

        # when
        result = get_description_for.iqa_from_tvoc(tvoc)

        # then
        self.assertEqual(expected_result, result)

    def test_invalid_brightness(self):
        # given
        brightness_level = 1000

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, '?')

    def test_white_brightness(self):
        # given
        brightness_level = 255

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'white')

    def test_very_bright_brightness(self):
        # given
        brightness_level = 225

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'very bright')


    def test_bright_brightness(self):
        # given
        brightness_level = 200
        expected_result = 'bright'

        # when
        result = get_description_for.brightness(brightness_level,brightness_level,brightness_level)

        # then
        self.assertEqual(expected_result,result)

    def test_bit_bright_brightness(self):
        # given
        brightness_level = 175

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'bit bright')

    def test_grey_brightness(self):
        # given
        brightness_level = 150

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'grey')

    def test_bit_dark_brightness(self):
        # given
        brightness_level = 100

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'bit dark')

    def test_dark_brightness(self):
        # given
        brightness_level = 72

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'dark')

    def test_very_dark_brightness(self):
        # given
        brightness_level = 24

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'very dark')

    def test_pitch_black_brightness(self):
        # given
        brightness_level = 8

        # when
        result = get_description_for.brightness(brightness_level, brightness_level, brightness_level)

        # then
        self.assertEqual(result, 'pitch black')

    def test_uv(self):
        # given
        scale_params_list = [(0, 'NONE'), (2, 'LOW'), (5, 'MEDIUM'), (7, 'HIGH'), (10, 'VERY HIGH'),
                             (20, 'EXTREME'),(-1,"UNKNOWN")]

        for an_input, expected_result in scale_params_list:
            with self.subTest(msg=f"Checking to get desciption for uv with value {an_input} "):
                # when
                result = get_description_for.uv(an_input)

                # debug
                print(f'for {an_input} result is {result} and expected result is {expected_result}')

                # then
                self.assertEqual(expected_result, result)

    def test_motion(self):
        # given
        motion_data = {
            'ax': 1.12,
            'ay': 1.13,
            'az': 1.14,
            'gx': 1.15,
            'gy': 1.16,
            'gz': 1.17,
            'mx': 1.18,
            'my': 1.19,
            'mz': 1.20
        }

        expected_result = 'Acc:   1.1   1.1   1.1 Gyro:   1.1   1.2   1.2 Mag:   1.2   1.2   1.2'

        # when
        result = get_description_for.motion(motion_data)

        # then
        self.assertEqual(expected_result, result)
