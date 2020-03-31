from unittest import TestCase

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
