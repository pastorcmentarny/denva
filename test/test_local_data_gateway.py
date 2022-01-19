import unittest

import config
from gateways import local_data_gateway


class LocalDataGatewayTestCases(unittest.TestCase):
    def test_get_data_for_non_working_url_should_return_error(self):
        if config_service.run_slow_test():
            # given
            url = 'http://192.168.0.204:5000/system'

            # when
            result = local_data_gateway.get_data_for(url)

            # then
            if 'error' not in result:
                self.fail()
        else:
            self.skipTest('running fast test only. local_data_gateway.get_data_for skipped.')
