from unittest import TestCase

from delight import delight_service
import system_data_service
import utils


class Test(TestCase):
    def test_run_gc(self):
        # given
        memory_available_in_mb = system_data_service.get_memory_available_in_mb()

        # when
        result = delight_service.run_gc()
        self.assertEqual(result['memory_before'],memory_available_in_mb)
        self.assertGreaterEqual(utils.get_int_number_from_text(result['memory_after']),utils.get_int_number_from_text(memory_available_in_mb) )
        self.assertGreaterEqual(result['memory_saved'],0)

        #debug
        print(result)

    def test_get_healthcheck(self):
        # given
        name = 'Denva Delight UI'
        expected_result = {'app': name, 'status': 'UP'}
        # when
        result = delight_service.get_healthcheck(name)
        # then
        self.assertEqual(result, expected_result)
