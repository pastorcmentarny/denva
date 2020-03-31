from unittest import TestCase

import config_serivce
import web_data


class Test(TestCase):

    # covers tube and trains (avoid to call web twice
    def test_get_status(self):
        if config_serivce.run_slow_test():
            # when
            result = web_data.get_status()

            # debug
            print(result)

            # then
            self.assertTrue('Tube data N/A' not in result)
            self.assertTrue('Train data N/A' not in result)
        else:
            self.skipTest('running fast test only. test_get_status skipped.')

    def test_get_crime(self):
        if config_serivce.run_slow_test():
            # when
            result = web_data.get_crime()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'Crime data N/A')
        else:
            self.skipTest('running fast test only. test_get_crime skipped.')

    def test_get_flood(self):
        if config_serivce.run_slow_test():
            # when
            result = web_data.get_flood()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'Flood data N/A')
        else:
            self.skipTest('running fast test only. test_get_flood skipped.')

    def test_get_weather(self):
        if config_serivce.run_slow_test():
            # when
            result = web_data.get_weather()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, ['Weather data N/A'])
        else:
            self.skipTest('running fast test only. test_get_weather skipped.')

    def test_get_o2_status(self):
        if config_serivce.run_slow_test():
            # when
            result = web_data.get_o2_status()

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'o2 data N/A')
        else:
            self.skipTest('running fast test only. test_get_o2_status skipped.')

    def test_get_pollution_for(self):
        if config_serivce.run_slow_test():
            # when
            result = web_data.get_pollution_for('wroclaw')

            # debug
            print(result)

            # then
            self.assertNotEqual(result, 'Pollution data N/A')
        else:
            self.skipTest('running fast test only. test_get_pollution_for skipped.')
