import unittest

from gateways import local_data_gateway


class LocalDataGatewayTests(unittest.TestCase):
    def test_get_data_for(self):
        # given
        url = 'http://192.168.0.204:5000/system'

        # when
        result = local_data_gateway.get_data_for(url)

        # debug
        if 'error' in result:
            print(':)')
