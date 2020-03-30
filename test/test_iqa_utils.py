import unittest

import iqa_utils


class MyTestCase(unittest.TestCase):

    def test_def_get_iqa_for_tvoc_for_radioactive_air(self):
        # given
        tvoc = '128256'
        expected_result = {
            'score': 'BAD',
            'value': int(tvoc),
            'action': 'Use only if unavoidable!',
            'information': 'Unacceptable Air Quality! Use only if unavoidable and only for short periods.'
        }

        # when
        result = iqa_utils.get_iqa_for_tvoc(tvoc)

        # then
        self.assertEqual(result, expected_result)

    def test_def_get_iqa_for_tvoc_for_clean_air(self):
        # given
        tvoc = '50'
        expected_result = {
            'score': 'Very Good',
            'value': int(tvoc),
            'action': 'No action required',
            'information': 'Clean air'
        }

        # when
        result = iqa_utils.get_iqa_for_tvoc(tvoc)

        # then
        self.assertEqual(result, expected_result)

    def test_def_get_iqa_for_tvoc_for_good_air(self):
        # given
        tvoc = '250'
        expected_result = {
            'score': 'Good',
            'value': int(tvoc),
            'action': 'Ventilation recommended.',
            'information': 'Good Air Quality'
        }

        # when
        result = iqa_utils.get_iqa_for_tvoc(tvoc)

        # then
        self.assertEqual(result, expected_result)

    def test_def_get_iqa_for_tvoc_for_medium_air(self):
        # given
        tvoc = '750'
        expected_result = {
            'score': 'Medium',
            'value': int(tvoc),
            'action': 'Ventilation required.',
            'information': 'Air Quality is not good. (Not recommended for exposure for than year)'
        }

        # when
        result = iqa_utils.get_iqa_for_tvoc(tvoc)

        # then
        self.assertEqual(result, expected_result)

    def test_def_get_iqa_for_tvoc_for_poor_air(self):
        # given
        tvoc = '3500'
        expected_result = {
            'score': 'POOR',
            'value': int(tvoc),
            'action': 'Ventilate now!',
            'information': 'Air Quality is POOR. (Not recommended for exposure for than month)'
        }

        # when
        result = iqa_utils.get_iqa_for_tvoc(tvoc)

        # then
        self.assertEqual(result, expected_result)
