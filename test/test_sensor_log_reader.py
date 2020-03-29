import unittest

import sensor_log_reader


class MyTestCase(unittest.TestCase):
    def test_get_denva_data_row_should_return_data_row_as_dict(self):
        # given
        expected_result = {'timestamp': '2020-03-27 16:33:13.050509', 'temp': '22.81', 'pressure': '1017.13',
                           'humidity': '27.269', 'gas_resistance': '12946860.59', 'colour': '#ff869f', 'aqi': 'n/a',
                           'uva_index': '0.00', 'uvb_index': '0.00', 'motion': '166.015625', 'ax': '0.01', 'ay': '0.01',
                           'az': '-0.00', 'gx': '0.54', 'gy': '1.45', 'gz': '0.08', 'mx': '-85.20', 'my': '29.10',
                           'mz': '-33.75', 'cpu_temp': '47.0', 'eco2': '744', 'tvoc': '476'}
        row = ['2020-03-27 16:33:13.050509', '22.81', '1017.13', '27.269', '12946860.59', '#ff869f', 'n/a', '0.0',
               '0.002591', '166.015625', '0.00732421875', '0.01318359375', '-0.00048828125', '0.5419847328244275',
               '1.450381679389313', '0.08396946564885496', '-85.2', '29.099999999999998', '-33.75', '1056', '47.0',
               '744', '476']

        print(row)

        # when
        result = sensor_log_reader.get_data_row(row)

        # debug
        print(result)

        # then
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
