import unittest

from services import spectrometer_service


class MyTestCase(unittest.TestCase):
    def test_check_warning_return_no_warning_for_valid_input(self):
        # given
        measurement = {
            "red": 3.6650288105010986,
            "orange": 1.8605425357818604,
            "yellow": 1.8842127323150635,
            "green": 1.0293954610824585,
            "blue": 1.3362101316452026,
            "violet": 0.0,
            "counter": 73197,
            "measurement_time": 265
        }
        expected_result = []

        # when
        result = spectrometer_service.check_warning(measurement)

        # debug
        print(result)

        # then
        self.assertEqual(len(result), 0)
        self.assertEqual(expected_result, result)

    def test_check_warning_return_1_warning_for_invalid_input(self):
        # given
        measurement = {
            "red": 0.0,
            "orange": 0.0,
            "yellow": 0.0,
            "green": 0.0,
            "blue": 0.0,
            "violet": 0.0,
            "counter": 73197,
            "measurement_time": 265
        }
        expected_result = [
            'Spectrometer returns zeros only Red:0.0 | Orange:0.0 | Yellow:0.0 | Green:0.0 | Blue:0.0 | Violet:0.0|']

        # when
        result = spectrometer_service.check_warning(measurement)

        # debug
        print(result)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
