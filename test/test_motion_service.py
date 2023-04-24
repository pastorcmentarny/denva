import unittest

from services import motion_service

test_data = [{'ax': -0.0302, 'ay': 0.3374, 'az': -0.3535, 'gx': 9.2519, 'gy': -11.9618, 'gz': -35.5954,
              'mx': -130.5, 'my': 159.75, 'mz': -424.2, 'counter': 1, 'measurement_time': 32},
             {'ax': -0.0244, 'ay': 0.6982, 'az': -0.4482, 'gx': 18.6259, 'gy': -9.1908, 'gz': -7.6793,
              'mx': -248.25, 'my': 228.15, 'mz': -557.6999, 'counter': 2, 'measurement_time': 19},
             {'ax': 0.165, 'ay': 0.4316, 'az': -0.2709, 'gx': 0.4351, 'gy': 12.8167, 'gz': 23.9083,
              'mx': 78.6, 'my': 136.0499, 'mz': -371.8499, 'counter': 3, 'measurement_time': 24}]


class MyTestCase(unittest.TestCase):
    def test_get_averages_as_dict(self):
        # given
        expected_result = {'ax': '0.04',
                           'ay': '0.49',
                           'az': '-0.36',
                           'gx': '9.44',
                           'gy': '-2.78',
                           'gz': '-6.46',
                           'measurement_time': '25.00',
                           'mx': '-100.05',
                           'my': '174.65',
                           'mz': '-451.25'}
        # when
        result = motion_service.get_averages_as_dict(test_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_get_records_as_dict(self):
        # given
        expected_result = {
            'lowest_ax': -0.0302,
            'highest_ax': 0.165,
            'lowest_ay': 0.3374,
            'highest_ay': 0.6982,
            'lowest_az': -0.4482,
            'highest_az': -0.2709,
            'lowest_gx': 0.4351,
            'highest_gx': 18.6259,
            'lowest_gy': -11.9618,
            'highest_gy': 12.8167,
            'lowest_gz': -35.5954,
            'highest_gz': 23.9083,
            'lowest_mx': -248.25,
            'highest_mx': 78.6,
            'lowest_my': 136.0499,
            'highest_my': 228.15,
            'lowest_mz': -557.6999,
            'highest_mz': -371.8499,
            'fastest_measurement_time': 19,
            'slowest_measurement_time': 32
        }

        # when
        result = motion_service.get_records_as_dict(test_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_check_warning_returns_all_warnings_for_to_high(self):
        # given
        expected_result = ['AX is high 3.11',
                           'AY is high 3.11',
                           'AZ is high 3.11',
                           'GX is high 3.11',
                           'GY is high 3.11',
                           'GZ is high 3.11',
                           'MX is high 150.5',
                           'MY is high 150.75',
                           'MZ is high 424.2']
        input_data = {'ax': 3.11, 'ay': 3.11, 'az': 3.11, 'gx': 3.11, 'gy': 3.11, 'gz': 3.11,
                      'mx': 150.5, 'my': 150.75, 'mz': 424.2}

        # when
        result = motion_service.check_warning(input_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
        self.assertEqual(len(expected_result), 9)

    def test_check_warning_returns_all_warnings_for_to_low(self):
        # given
        expected_result = ['AX is high -3.11',
                           'AY is high -3.11',
                           'AZ is high -3.11',
                           'GX is high -3.11',
                           'GY is high -3.11',
                           'GZ is high -3.11',
                           'MX is high 110.5',
                           'MY is high 110.75',
                           'MZ is high -424.2']
        input_data = {'ax': -3.11, 'ay': -3.11, 'az': -3.11, 'gx': -3.11, 'gy': -3.11, 'gz': -3.11,
                      'mx': 110.5, 'my': 110.75, 'mz': -424.2}

        # when
        result = motion_service.check_warning(input_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
        self.assertEqual(len(expected_result), 9)

    def test_check_warning_returns_empty_for_no_warnings(self):
        # given
        expected_result = []
        input_data = {'ax': 0.1, 'ay': -0.1, 'az': -0.1, 'gx': 0.11, 'gy': -0.11, 'gz': -0.12,
                      'mx': -70.5, 'my': 130.75, 'mz': -360.2}

        # when
        result = motion_service.check_warning(input_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
        self.assertEqual(len(expected_result), 0)


if __name__ == '__main__':
    unittest.main()
