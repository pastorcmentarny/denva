from unittest import TestCase

import config_service


class Test(TestCase):
    def test_get_irregular_verbs_path(self):
        # when
        result = config_service.get_irregular_verbs_path()

        # then
        self.assertTrue(result.endswith('data/irregular_verbs.txt'))

    def test_get_shaking_level(self):
        # when
        result = config_service.get_shaking_level()

        # then
        self.assertEqual(result, 1000)

    # TODO change it if i want run autotest on the server device
    def test_set_mode_to(self):
        # when
        config_service.set_mode_to('server')

        # then
        self.assertEqual(config_service.get_mode(), 'dev')

    def test_get_data_path(self):
        # when
        result = config_service.get_data_path()

        # then
        self.assertEqual("D:\\denva\\data\\", result)
