from unittest import TestCase

import enviro_service
import system_data_service
import utils

class Test(TestCase):
    def test_run_gc_in_enviro_service(self):
        # given
        memory_available_in_mb = system_data_service.get_memory_available_in_mb()

        # when
        result = enviro_service.run_gc()
        self.assertEqual(result['memory_before'],memory_available_in_mb)
        self.assertGreaterEqual(utils.get_int_number_from_text(result['memory_after']),utils.get_int_number_from_text(memory_available_in_mb) )
        self.assertGreaterEqual(result['memory_saved'],0)

        #debug
        print(result)


