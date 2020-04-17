from unittest import TestCase
from unittest.mock import Mock

from reports import report_generator


class Test(TestCase):
    def test_read_data_as_list_from_csv_file_for_denva(self):
        # given
        line = '2020-03-27 16:33:13.050509,22.81,1017.13,27.269,12946860.59,#ff869f,n/a,0.0,0.002591,166.015625,0.00732421875,0.01318359375,-0.00048828125,0.5419847328244275,1.450381679389313,0.08396946564885496,-85.2,29.099999999999998,-33.75,1056,47.0,744,476'.split(
            ',')
        line2 = '2020-03-27 16:33:21.516359,22.82,1017.14,27.162,12946860.59,#ff869f,n/a,0.0,0.002591,146.484375,0.0009765625,0.0078125,0.02392578125,0.6946564885496184,1.786259541984733,-0.030534351145038167,-84.75,30.299999999999997,-34.05,1035,48.0,805,478'.split(
            ',')
        test_data = [line, line2]
        report_generator.read_data_as_list_from_csv_file = Mock(return_value=test_data)

        expected_result = [
            {'timestamp': '2020-03-27 16:33:13.050509', 'temp': '22.81', 'pressure': '1017.13', 'humidity': '27.269',
             'gas_resistance': '12946860.59', 'colour': '#ff869f', 'aqi': 'n/a', 'uva_index': '0.0',
             'uvb_index': '0.002591', 'motion': '166.015625', 'ax': '0.00732421875', 'ay': '0.01318359375',
             'az': '-0.00048828125', 'gx': '0.5419847328244275', 'gy': '1.450381679389313', 'gz': '0.08396946564885496',
             'mx': '-85.2', 'my': '29.099999999999998', 'mz': '-33.75', 'measurement_time': '1056', 'cpu_temp': '47.0',
             'eco2': '744', 'tvoc': '476'},
            {'timestamp': '2020-03-27 16:33:21.516359', 'temp': '22.82', 'pressure': '1017.14', 'humidity': '27.162',
             'gas_resistance': '12946860.59', 'colour': '#ff869f', 'aqi': 'n/a', 'uva_index': '0.0',
             'uvb_index': '0.002591', 'motion': '146.484375', 'ax': '0.0009765625', 'ay': '0.0078125',
             'az': '0.02392578125', 'gx': '0.6946564885496184', 'gy': '1.786259541984733',
             'gz': '-0.030534351145038167', 'mx': '-84.75', 'my': '30.299999999999997', 'mz': '-34.05',
             'measurement_time': '1035', 'cpu_temp': '48.0', 'eco2': '805', 'tvoc': '478'}]

        # when
        result = report_generator.load_data(2020, 3, 27)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_read_data_as_list_from_csv_file_for_enviro(self):
        # given
        line = '2020-03-27 13:44:09.656392,14.859722079502383,1017.3365492766806,12.456811542625449,24.473,0,92.0769230769231,224.0000000000001,135.304347826087,18.0,27.0,27.0,330'.split(
            ',')
        line2 = '2020-03-27 13:44:55.500674,15.029733518857633,1017.3268359204353,12.457866558726307,30.7063,0,92.43373493975908,224.0000000000001,135.304347826087,19.0,29.0,29.0,335'.split(
            ',')
        test_data = [line, line2]
        report_generator.read_data_as_list_from_csv_file = Mock(return_value=test_data)

        expected_result = [
            {'timestamp': '2020-03-27 13:44:09.656392', 'temperature': '14.9', 'light': '24.5', 'oxidised': '92.08',
             'reduced': '224.00', 'nh3': '135.30', 'pm1': '18.0', 'pm25': '27.0', 'pm10': '27.0',
             'measurement_time': '330'},
            {'timestamp': '2020-03-27 13:44:55.500674', 'temperature': '15.0', 'light': '30.7', 'oxidised': '92.43',
             'reduced': '224.00', 'nh3': '135.30', 'pm1': '19.0', 'pm25': '29.0', 'pm10': '29.0',
             'measurement_time': '335'}]

        # when
        result = report_generator.load_enviro_data(2020, 3, 27)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
