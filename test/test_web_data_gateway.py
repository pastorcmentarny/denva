import unittest
from unittest import TestCase

import config
from gateways import web_data_gateway


class WebDataGatewayTestCases(TestCase):

    # covers tube and trains (avoid to call web twice
    def test_get_status(self):
        if config.run_slow_test():
            # when
            result = web_data_gateway.get_status()

            # debug
            print(result)

            # then
            self.assertTrue('Tube data N/A' not in result)
            self.assertTrue('Train data N/A' not in result)
        else:
            self.skipTest('running fast test only. test_get_status skipped.')

    @unittest.skip("COVID-19")  # TODO this test failing as service is unavailable due to COVID-19
    def test_get_crime(self):
        if config.run_slow_test():
            # when
            result = web_data_gateway.get_crime()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'Crime data N/A')
        else:
            self.skipTest('running fast test only. test_get_crime skipped.')

    def test_get_flood(self):
        if config.run_slow_test():
            # when
            result = web_data_gateway.get_flood()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'Flood data N/A')
        else:
            self.skipTest('running fast test only. test_get_flood skipped.')

    def test_get_weather(self):
        if config.run_slow_test():
            # when
            result = web_data_gateway.get_weather()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, ['Weather data N/A'])
        else:
            self.skipTest('running fast test only. test_get_weather skipped.')

    def test_get_o2_status(self):
        if config.run_slow_test():
            # when
            result = web_data_gateway.get_o2_status()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'o2 data N/A')
        else:
            self.skipTest('running fast test only. test_get_o2_status skipped.')

    def test_get_pollution_for(self):
        if config.run_slow_test():
            # when
            result = web_data_gateway.get_pollution_for('wroclaw')

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'Pollution data N/A')
        else:
            self.skipTest('running fast test only. test_get_pollution_for skipped.')

    # parameterized-unit-test in python example
    def test___get_scale_result_from_should_return_hazard(self):
        # given
        scale_params_list = [(500, 'At Aberystwyth, pollution level is Hazardous! (500).Stay at home!'),
                             (250, 'At Aberystwyth, pollution level is Unhealthy (250).Should stay at home.'),
                             (125, 'At Aberystwyth, pollution level is Moderate (125).Limit prolong outdoor activity.'),
                             (50, 'At Aberystwyth, pollution level is Good (50).')]

        for input, expected_result in scale_params_list:
            with self.subTest(msg="Checking _get_scale_result_from() for scale {} "(input)):
                # when
                result = web_data_gateway._get_scale_result_from('aberystwyth', input)

                # debug
                print(result)

                # then
                self.assertEqual(expected_result, result)

    def test_get_iss_location(self):
        # when
        result = web_data_gateway.get_iss_location()

        # debug
        print(result)

        # then
        self.assertEqual(result['message'], 'success')


# run this file test only
if __name__ == '__main__':
    unittest.main()
