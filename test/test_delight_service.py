from unittest import TestCase

import config_service
from utils import dom_utils
from delight import delight_service
from services import system_data_service


class Test(TestCase):
    def test_run_gc(self):
        if config_service.run_slow_test():
            # given
            memory_available_in_mb = system_data_service.get_memory_available_in_mb()

            # when
            result = delight_service.run_gc()
            self.assertEqual(result['memory_before'], memory_available_in_mb)
            self.assertGreaterEqual(dom_utils.get_int_number_from_text(result['memory_after']),
                                    dom_utils.get_int_number_from_text(memory_available_in_mb))
            self.assertGreaterEqual(result['memory_saved'], 0)

            # debug
            print(result)
        else:
            self.skipTest('running fast test only. test_network_check_should_return_perfect skipped.')


def test_get_healthcheck(self):
    # given
    name = 'Denva Delight UI'
    expected_result = {'app': name, 'status': 'UP'}
    # when
    result = delight_service.get_healthcheck(name)
    # then
    self.assertEqual(expected_result, result)
