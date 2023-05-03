import unittest

from services import gps_service

test_data = [
    {"timestamp": "20230503-091512", "latitude": 0.0, "longitude": 0.0, "altitude": None, "lat_dir": "", "lon_dir": "", "geo_sep": "",
     "num_sats": 1, "gps_qual": 0, "speed_over_ground": 0.0, "mode_fix_type": "1", "pdop": "", "hdop": "", "vdop": "", "counter": 1,
     "measurement_time": 169},
    {"timestamp": "20230503-091512", "latitude": 0.0, "longitude": 0.0, "altitude": None, "lat_dir": "", "lon_dir": "", "geo_sep": "",
     "num_sats": 1, "gps_qual": 0, "speed_over_ground": 0.0, "mode_fix_type": "1", "pdop": "", "hdop": "", "vdop": "", "counter": 1,
     "measurement_time": 122},
    {"timestamp": "20230503-091513", "latitude": 0.0, "longitude": 0.0, "altitude": None, "lat_dir": "", "lon_dir": "", "geo_sep": "",
     "num_sats": 0, "gps_qual": 0, "speed_over_ground": 0.0, "mode_fix_type": "1", "pdop": "", "hdop": "", "vdop": "", "counter": 2,
     "measurement_time": 105},
    {"timestamp": "20230503-091513", "latitude": 0.0, "longitude": 0.0, "altitude": None, "lat_dir": "", "lon_dir": "", "geo_sep": "",
     "num_sats": 0, "gps_qual": 0, "speed_over_ground": 0.0, "mode_fix_type": "1", "pdop": "", "hdop": "", "vdop": "", "counter": 3,
     "measurement_time": 118},
]


class MyTestCase(unittest.TestCase):
    def test_get_averages_as_dict(self):
        # given
        expected_result = {'num_sats': 0.5}
        # when
        result = gps_service.get_averages_as_dict(test_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_get_records_as_dict(self):
        # given
        expected_result = {
            'max_num_sats': 1,
            'gps_fastest_measurement_time': 105,
            'gps_slowest_measurement_time': 169
        }

        # when
        result = gps_service.get_records_as_dict(test_data)

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_check_warning_returns_all_warnings_for_to_low(self):
        # given
        expected_result = ['GPS not detecting any satellites.']

        # when
        result = gps_service.get_warnings(test_data[2])

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
        self.assertEqual(len(expected_result), 1)

    def test_check_warning_returns_empty_for_no_warnings(self):
        # given
        expected_result = []

        # when
        result = gps_service.get_warnings(test_data[0])

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
        self.assertEqual(len(expected_result), 0)


if __name__ == '__main__':
    unittest.main()
