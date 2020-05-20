import unittest
from unittest.mock import patch

from common import loggy


class LoggyTestCase(unittest.TestCase):
    # tag-test-logger
    @patch('logging.Logger.debug')
    def test_log_error_count_should_log_no_errors(self, mock_logger):
        # when
        loggy.log_error_count([])

        # then
        mock_logger.assert_called_with('No errors found.')
