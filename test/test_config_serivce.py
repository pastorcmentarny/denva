from unittest import TestCase

import config_serivce


class Test(TestCase):
    def test_get_shaking_level(self):
        # when
        result = config_serivce.get_shaking_level()

        # then
        self.assertEqual(result, 1000)
