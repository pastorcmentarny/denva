import unittest

from denviro import denviro_sensors_service

ENVIRO_ROW = ['2020-03-27 13:44:09.656392', '14.859722079502383', '1017.3365492766806', '12.456811542625449', '24.473',
              '0', '92.0769230769231', '224.0000000000001', '135.304347826087', '18.0', '27.0', '27.0', '330', '21.6']


class DenviroSensorTestCases(unittest.TestCase):
    def test_add_row_for_enviro_will_increase_list_to_one(self):
        # given
        data = []

        # when
        self.assertEqual(len(data), 0)
        denviro_sensors_service.add_enviro_row(data, ENVIRO_ROW)

        # then
        self.assertEqual(len(data), 1)

    def test_get_enviro_data_row_should_return_data_row_as_dict(self):
        # given
        expected_result = {'timestamp': '2020-03-27 13:44:09.656392', 'temperature': '14.9', 'light': '24.5',
                           'oxidised': '92.08',
                           'reduced': '224.00', 'nh3': '135.30', 'pm1': '18.0', 'pm25': '27.0', 'pm10': '27.0',
                           'measurement_time': '330', 'cpu_temp': '21.6'}

        # when
        result = denviro_sensors_service.get_data_row(ENVIRO_ROW)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
