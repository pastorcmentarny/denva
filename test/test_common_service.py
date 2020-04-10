from unittest import TestCase

import common_service
import config_service
import system_data_service
import utils


class Test(TestCase):
    def test_run_gc_in_server_service(self):
        if config_service.run_slow_test():
            # given
            memory_available_in_mb = system_data_service.get_memory_available_in_mb()

            # when
            result = common_service.run_gc()

            # then
            self.assertEqual(result['memory_before'], memory_available_in_mb)
            self.assertLessEqual(utils.get_int_number_from_text(result['memory_after']),
                                 utils.get_int_number_from_text(memory_available_in_mb))
            self.assertGreaterEqual(result['memory_saved'], 0)
        else:
            self.skipTest('running fast test only. test_network_check_should_return_perfect skipped.')
