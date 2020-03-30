from unittest import TestCase

import config_serivce


class Test(TestCase):
    def test_get_irregular_verbs_path(self):
        # when
        result = config_serivce.get_irregular_verbs_path()

        # then
        self.assertTrue(result.endswith('data/irregular_verbs.txt'))


    def test_get_shaking_level(self):
        # when
        result = config_serivce.get_shaking_level()

        # then
        self.assertEqual(result, 1000)
