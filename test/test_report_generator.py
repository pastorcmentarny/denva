from unittest import TestCase
from unittest.mock import Mock
import report_generator


class Test(TestCase):
    def test_network_check_should_return_perfect(self):
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
        self.assertEqual(result, expected_result)
