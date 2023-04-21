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


if __name__ == '__main__':
    unittest.main()
