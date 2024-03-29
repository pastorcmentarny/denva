from unittest import TestCase

import dom_utils
from services import system_data_service


class SystemDataServiceTestCases(TestCase):
    # this is temporary test
    def test_get_system_information_should_return_data(self):
        # given
        memory_available_in_mb = system_data_service.get_memory_available_in_mb()

        # when
        result = system_data_service.get_system_information()

        # debug
        print(result)

        # then
        self.assertEqual(len(result), 4)
        self.assertGreaterEqual(dom_utils.get_int_number_from_text(result['CPU Speed']), 200)
        self.assertGreaterEqual(dom_utils.get_int_number_from_text(result['Memory Available']), 200)
        self.assertGreaterEqual(dom_utils.get_int_number_from_text(result['Disk Free']), 200)
        self.assertTrue(result['Uptime'])
