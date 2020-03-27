from unittest import TestCase

import enviro_service
import system_data_service


class Test(TestCase):
    # this is temporary test
    def test_run_gc_in_server_service(self):
        result = enviro_service.run_gc()
        memory_available_in_mb = system_data_service.get_memory_available_in_mb()
        self.assertEqual(result['memory_before'],memory_available_in_mb)
        self.assertEqual(result['memory_after'],memory_available_in_mb)
        self.assertEqual(result['memory_saved'],0)

        #debug
        print(result)


