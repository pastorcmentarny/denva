import unittest

from services import log_metrics_service

TEST_PATH = 'B:\\GitHub\\denva\\resources_data\\test-log.txt'


class LogMetricsTestCases(unittest.TestCase):

    def test_generate_log_stats(self):
        # given
        log_metrics_service.clear()

        expected_result = {'CRITICAL': 17,
                           'DEBUG': 0,
                           'ERROR': 12,
                           'INFO': 83633,
                           'WARNING': 1,
                           'total_count': 83663}
        # when
        log_metrics_service.generate_log_stats(TEST_PATH)

        # then
        self.assertEqual(log_metrics_service.get_log_metrics(), expected_result)

    def test_get_stats_for(self):
        # given
        log_metrics_service.clear()

        log_metrics_service.generate_log_stats(TEST_PATH)
        expected_result = 'error count: 12 which is 0.01% of all logs.'
        # when
        result = log_metrics_service.get_stats_for('ERROR')

        # then
        self.assertEqual(result, expected_result)

    def test_clear(self):
        # given
        log_metrics_service.clear()
        log_metrics_service.generate_log_stats(TEST_PATH)
        verify_data = {'CRITICAL': 17,
                       'DEBUG': 0,
                       'ERROR': 12,
                       'INFO': 83633,
                       'WARNING': 1,
                       'total_count': 83663}
        expected_result = {'CRITICAL': 0,
                           'DEBUG': 0,
                           'ERROR': 0,
                           'INFO': 0,
                           'WARNING': 0,
                           'total_count': 0}
        # verify
        log_metrics_data = log_metrics_service.get_log_metrics()
        self.assertEqual(log_metrics_data, verify_data)

        # when
        log_metrics_service.clear()
        result = log_metrics_service.get_log_metrics()

        # then
        self.assertNotEquals(result, verify_data)
        self.assertEqual(result,expected_result)


if __name__ == '__main__':
    unittest.main()
