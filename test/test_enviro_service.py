from unittest import TestCase

import enviro_service


class Test(TestCase):
    def test_run_gc(self):
        result = enviro_service.run_gc()
        self.assertEqual(result['memory_saved'],0)

        #debug
        print(result)


