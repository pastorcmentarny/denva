from datetime import date
from unittest import TestCase
from unittest.mock import patch

import utils


class Test(TestCase):

    def test_get_int_number_from_text(self):
        self.assertEqual(utils.get_int_number_from_text('250MB'), 250)

    def test_get_int_number_from_text_should_return_int_without_text(self):
        self.assertEqual(utils.get_int_number_from_text('125'), 125)

    def test_get_float_number_from_text(self):
        self.assertEqual(utils.get_float_number_from_text('2.1 kB'), '2.1')

    def test_get_float_number_from_text_should_return_int_without_text(self):
        self.assertEqual(utils.get_float_number_from_text('2.1'), '2.1')

    def test_to_hex(self):
        # given
        expected_result = '#ff800f'

        # when
        result = utils.to_hex(255, 128, 15)

        # then
        self.assertEqual(result, expected_result)

    def test_convert_list_to_dict(self):
        # given
        example_list = ['one', 'two', 'three']
        expected_result = {
            '001': 'one',
            '002': 'two',
            '003': 'three'
        }

        # when
        result = utils.convert_list_to_dict(example_list)

        # then
        self.assertEqual(result, expected_result)

    # tag-mock-date
    def test_get_date_as_folders(self):
        # given
        with patch('utils.date') as mock_date:
            mock_date.today.return_value = date(2006, 6, 6)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            # verify that mock works
            assert utils.date.today() == date(2006, 6, 6)

            expected_result = '\\2006\\06\\06\\'

            # when
            result = utils.get_date_as_folders()

            # then
            self.assertEqual(result, expected_result)
