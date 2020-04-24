from datetime import date, datetime
from unittest import TestCase
from unittest.mock import patch

from common import gobshite_exception, dom_utils


class Test(TestCase):

    def test_get_int_number_from_text(self):
        self.assertEqual(dom_utils.get_int_number_from_text('250MB'), 250)

    def test_get_int_number_from_text_should_return_int_without_text(self):
        self.assertEqual(dom_utils.get_int_number_from_text('125'), 125)

    def test_get_float_number_from_text(self):
        self.assertEqual(dom_utils.get_float_number_from_text('2.1 kB'), '2.1')

    def test_get_float_number_from_text_should_return_int_without_text(self):
        self.assertEqual(dom_utils.get_float_number_from_text('2.1'), '2.1')

    def test_to_hex(self):
        # given
        expected_result = '#ff800f'

        # when
        result = dom_utils.to_hex(255, 128, 15)

        # then
        self.assertEqual(expected_result, result)

    def test_convert_list_to_dict(self):
        # given
        example_list = ['one', 'two', 'three']
        expected_result = {
            '001': 'one',
            '002': 'two',
            '003': 'three'
        }

        # when
        result = dom_utils.convert_list_to_dict(example_list)

        # then
        self.assertEqual(expected_result, result)

    # tag-mock-date
    def test_get_date_as_folders(self):
        # given
        with patch('common.dom_utils.date') as mock_date:
            mock_date.today.return_value = date(2006, 6, 6)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            # verify that mock works
            assert dom_utils.date.today() == date(2006, 6, 6)

            expected_result = '\\2006\\06\\06\\'

            # when
            result = dom_utils.get_date_as_folders()

            # then
            self.assertEqual(expected_result, result)

    def test_get_timestamp_title_with_time(self):
        # given
        with patch('common.dom_utils.datetime') as mock_date:
            mock_date.now.return_value = datetime(2006, 6, 6, 10, 10, 10)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            # verify that mock works
            assert dom_utils.datetime.now() == datetime(2006, 6, 6, 10, 10, 10)

            expected_result = '2006-06-06 10:10:10'

            # when
            result = dom_utils.get_timestamp_title(with_time=True)

            # then
            self.assertEqual(expected_result, result)

    def test_get_timestamp_title_without_time(self):
        # given
        with patch('common.dom_utils.datetime') as mock_date:
            mock_date.now.return_value = datetime(2006, 6, 6)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)

            # verify that mock works
            assert dom_utils.datetime.now() == datetime(2006, 6, 6)

            expected_result = '2006-06-06'

            # when
            result = dom_utils.get_timestamp_title(with_time=False)

            # then
            self.assertEqual(expected_result, result)

    def test_convert_time_to_minutes(self):
        scale_params_list = [('00:00 - Sleep', 0), ('0:00 - Sleep', 0), ('1:00 - Sleep', 60), ('12:00 - Sleep', 720),
                             ('23:59 - Sleep', 1439)]

        for an_input, expected_result in scale_params_list:
            with self.subTest(msg="Checking to convert_time_to_minutes() for event {} ".format(an_input)):
                # when
                result = dom_utils.convert_time_to_minutes(an_input)

                # debug
                print('for {} result is {} and expected result is {}'.format(an_input, result, expected_result))

                # then
                self.assertEqual(expected_result, result)

    def test_convert_time_to_minutes_should_throw_exception_for_invalid_input(self):
        scale_params_list = ['00:0 - Sleep', '0.00 - Sleep', '0:00:01 - Sleep', 'Sleep', 'a0:0 - Sleep', '0:0a - Sleep',
                             '0:00', '0:00 Sleep', None, '', ' ', '0000:00 - Sleep', '00:0000 - Sleep', '24:00 - Sleep',
                             '23:61 - Sleep']

        for an_input in scale_params_list:
            with self.subTest(
                    msg="Checking to convert_time_to_minutes() for event {} should throw exception ".format(an_input)):
                # when
                self.assertRaises(gobshite_exception.GobshiteException, dom_utils.convert_time_to_minutes, an_input)

    def test_is_weekend_day_is_true_for_saturday(self):
        # given
        saturday = datetime(2020, 4, 11, 0, 0, 0)

        # when
        result = dom_utils.is_weekend_day(saturday)

        # then
        self.assertTrue(result)

    def test_is_weekend_day_is_true_for_monday(self):
        # given
        monday = datetime(2020, 4, 13, 0, 0, 0)

        # when
        result = dom_utils.is_weekend_day(monday)

        # then
        self.assertFalse(result)
