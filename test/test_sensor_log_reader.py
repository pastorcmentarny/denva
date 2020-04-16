import unittest

import sensor_log_reader

DENVA_ROW = ['2020-03-27 16:33:13.050509', '22.81', '1017.13', '27.269', '12946860.59', '#ff869f', 'n/a', '0.0',
             '0.002591', '166.015625', '0.00732421875', '0.01318359375', '-0.00048828125', '0.5419847328244275',
             '1.450381679389313', '0.08396946564885496', '-85.2', '29.099999999999998', '-33.75', '1056', '47.0',
             '744', '476']

ENVIRO_ROW = ['2020-03-27 13:44:09.656392', '14.859722079502383', '1017.3365492766806', '12.456811542625449', '24.473',
              '0', '92.0769230769231', '224.0000000000001', '135.304347826087', '18.0', '27.0', '27.0', '330', '21.6']


class MyTestCase(unittest.TestCase):

    def test_add_row_for_denva_will_increase_list_to_one(self):
        # given
        data = []

        # when
        self.assertEqual(len(data), 0)
        sensor_log_reader.add_row(data, DENVA_ROW)

        # then
        self.assertEqual(len(data), 1)

    def test_get_denva_data_row_should_return_data_row_as_dict(self):
        # given
        expected_result = {'timestamp': '2020-03-27 16:33:13.050509', 'temp': '22.81', 'pressure': '1017.13',
                           'humidity': '27.269', 'gas_resistance': '12946860.59', 'colour': '#ff869f', 'aqi': 'n/a',
                           'uva_index': '0.00', 'uvb_index': '0.00', 'motion': '166.015625', 'ax': '0.01', 'ay': '0.01',
                           'az': '-0.00', 'gx': '0.54', 'gy': '1.45', 'gz': '0.08', 'mx': '-85.20', 'my': '29.10',
                           'mz': '-33.75', 'cpu_temp': '47.0', 'eco2': '744', 'tvoc': '476'}

        # when
        result = sensor_log_reader.get_data_row(DENVA_ROW)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_add_row_for_enviro_will_increase_list_to_one(self):
        # given
        data = []

        # when
        self.assertEqual(len(data), 0)
        sensor_log_reader.add_enviro_row(data, ENVIRO_ROW)

        # then
        self.assertEqual(len(data), 1)

    def test_get_enviro_data_row_should_return_data_row_as_dict(self):
        # given
        expected_result = {'timestamp': '2020-03-27 13:44:09.656392', 'temperature': '14.9', 'light': '24.5',
                           'oxidised': '92.08',
                           'reduced': '224.00', 'nh3': '135.30', 'pm1': '18.0', 'pm25': '27.0', 'pm10': '27.0',
                           'measurement_time': '330', 'cpu_temp': '21.6'}

        # when
        result = sensor_log_reader.get_data_row_for_enviro(ENVIRO_ROW)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
