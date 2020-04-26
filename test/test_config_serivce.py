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

    def test_get_environment_log_path_for(self):
        # given
        scale_params_list = [('denva', 'app', '/home/pi/denva-master/src/configs/log_app_config.json'),
                             ('denva', 'ui', '/home/pi/denva-master/src/configs/log_ui_config.json'),
                             ('dev', 'app', 'D:\Projects\denva\src\configs\dev_log_app_config.json'),
                             ('dev', 'ui', 'D:\Projects\denva\src\configs\dev_log_ui_config.json'),
                             ('server', 'app', 'E:\denva\src\configs\mothership_log_app_config.json'),
                             ('server', 'ui', 'E:\denva\src\configs\mothership_log_ui_config.json')]

        for mode, an_input, expected_result in scale_params_list:
            with self.subTest(msg="Checking to get_environment_log_path_for() for case {} ".format(an_input)):
                # given
                config_service.load_cfg()['mode'] = mode
                # when
                result = config_service.get_environment_log_path_for(an_input)

                # then
                self.assertEqual(expected_result, result)
