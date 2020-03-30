from unittest import TestCase

import records


class Test(TestCase):
    def test_get_denva_records_should_return_records(self):
        data = [
            {'timestamp': '2020-03-27 16:33:13.050509', 'temperature': '22.81', 'pressure': '1017.13', 'humidity': '27.269',
             'gas_resistance': '12946860.59', 'colour': '#ff869f', 'aqi': 'n/a', 'uva_index': '0.0',
             'uvb_index': '0.002591', 'motion': '166.015625', 'ax': '0.00732421875', 'ay': '0.01318359375',
             'az': '-0.00048828125', 'gx': '0.5419847328244275', 'gy': '1.450381679389313', 'gz': '0.08396946564885496',
             'mx': '-85.2', 'my': '29.099999999999998', 'mz': '-33.75', 'measurement_time': '1056', 'cpu_temp': '47.0',
             'eco2': '744', 'tvoc': '476'},
            {'timestamp': '2020-03-27 16:33:21.516359', 'temperature': '22.82', 'pressure': '1017.14', 'humidity': '27.162',
             'gas_resistance': '12946860.59', 'colour': '#ff869f', 'aqi': 'n/a', 'uva_index': '0.0',
             'uvb_index': '0.002591', 'motion': '146.484375', 'ax': '0.0009765625', 'ay': '0.0078125',
             'az': '0.02392578125', 'gx': '0.6946564885496184', 'gy': '1.786259541984733',
             'gz': '-0.030534351145038167', 'mx': '-84.75', 'my': '30.299999999999997', 'mz': '-34.05',
             'measurement_time': '1035', 'cpu_temp': '48.0', 'eco2': '805', 'tvoc': '478'}]
        expected_result = {'temperature': {'min': '22.81', 'max': '22.82'},
                           'pressure': {'min': '1017.13', 'max': '1017.14'},
                           'humidity': {'min': '27.162', 'max': '27.269'}, 'max_uv_index': {'uva': 0.0, 'uvb': 0.0},
                           'cpu_temperature': {'min': '47.0', 'max': '48.0'}, 'biggest_motion': '166',
                           'highest_eco2': '805', 'highest_tvoc': '478', 'log entries counter': 2,
                           'execution_time': '0 ns.'}

        # when
        result = records.get_records(data)
        result['execution_time'] = '0 ns.' #not part of the test

        # debug
        print(result)

        # then
        self.assertEqual(result, expected_result)

    def test_get_enviro_records_should_return_records(self):
        # given
        data = [
            {'timestamp': '2020-03-27 13:44:09.656392', 'temperature': '14.8', 'light': '24.5', 'oxidised': '92.08',
             'reduced': '224.00', 'nh3': '135.30', 'pm1': '18.0', 'pm25': '27.0', 'pm10': '27.0',
             'measurement_time': '330'},
            {'timestamp': '2020-03-27 13:44:55.500674', 'temperature': '15.0', 'light': '30.7', 'oxidised': '92.43',
             'reduced': '224.00', 'nh3': '135.30', 'pm1': '19.0', 'pm25': '30.0', 'pm10': '29.0',
             'measurement_time': '335'}]
        expected_result = {'temperature': {'min': '14.8', 'max': '15.0'}, 'highest_light': '30.7',
                           'highest_oxidised': '92.43', 'highest_reduced': '224.00', 'highest_pm1': '19.0',
                           'highest_pm25': '30.0', 'highest_pm10': '29.0',
                           'measurement_time': {'min': '330', 'max': '335'}, 'log entries counter': 2,
                           'execution_time': '0 ns.'}

        # when
        result = records.get_enviro_records(data)
        result['execution_time'] = '0 ns.' # as execution vary per run
        # debug
        print(result)

        # then
        self.assertEqual(result, expected_result)
