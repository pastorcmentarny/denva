import unittest
from datetime import datetime
from datetime import timedelta
from unittest import TestCase

from systemhc import system_health_check_service


class SystemHealthTest(TestCase):

    def test_get_status(self):
        params_list = [[datetime.now(), 'UP'],
                       [datetime.now() + timedelta(seconds=-55), 'UP'],
                       [datetime.now() + timedelta(minutes=-2, seconds=-55), 'WARN'],
                       [datetime.now() + timedelta(minutes=-5, seconds=-1), 'DOWN']

                       ]

        for an_input, expected_result in params_list:
            with self.subTest(msg=" get_status() for {} should return {}".format(an_input, expected_result)):
                # when
                result = system_health_check_service.get_status(an_input)

                # then
                self.assertEqual(expected_result, result)

    @unittest.skip("need to change setup for this test")
    def test_get_system_healthcheck_where_everything_is_down(self):
        # given
        expected_result = {'denva': {'app': 'DOWN', 'ui': 'DOWN'}, 'denviro': {'app': 'DOWN', 'ui': 'DOWN'},
                           'delight': {'app': 'DOWN', 'ui': 'DOWN'}, 'server': {'app': 'DOWN', 'ui': 'DOWN'},
                           'other': {'cctv': 'DOWN', 'radar': 'DOWN', 'digest': 'DOWN'}}

        # when
        result = system_health_check_service.get_system_healthcheck()

        # then
        self.assertEqual(expected_result, result)

    def test_get_system_healthcheck_where_everything_is_up(self):
        # given
        expected_result = {'denva': {'app': 'UP', 'ui': 'UP'}, 'denviro': {'app': 'UP', 'ui': 'UP'},
                           'delight': {'app': 'UP', 'ui': 'UP'}, 'server': {'app': 'UP', 'ui': 'UP'},
                           'other': {'cctv': 'OFF', 'radar': 'OFF', 'digest': 'UP'}}
        system_health_check_service.update_to_now_for_all()
        # when

        result = system_health_check_service.get_system_healthcheck()

        # then
        self.assertEqual(expected_result, result)
