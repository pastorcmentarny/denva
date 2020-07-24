from unittest import TestCase

import config_service


class Test(TestCase):
    def test_get_irregular_verbs_path(self):
        # given
        config_service.set_mode_to('dev')

        # when
        result = config_service.get_irregular_verbs_path()

        # then
        self.assertTrue(result.endswith('data/irregular_verbs.txt'))

    def test_get_shaking_level(self):
        # when
        result = config_service.get_shaking_level()

        # then
        self.assertEqual(result, 1000)

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
                             ('dev', 'app', 'D:\GitHub\denva\src\configs\dev_log_app_config.json'),
                             ('dev', 'ui', 'D:\GitHub\denva\src\configs\dev_log_ui_config.json'),
                             ('server', 'app', 'E:\denva\src\configs\server_log_app_config.json'),
                             ('server', 'ui', 'E:\denva\src\configs\server_log_ui_config.json'),
                             ('dev', 'ddd', 'D:\GitHub\denva\src\configs\dev_log_app_config.json'),
                             ('ddd', 'ddd', 'D:\GitHub\denva\src\configs\dev_log_app_config.json')]

        for mode, an_input, expected_result in scale_params_list:
            with self.subTest(
                    msg="Checking to get_environment_log_path_for() for mode {} & app type {} ".format(mode, an_input)):
                # given
                config_service.load_cfg()['mode'] = mode
                # when
                result = config_service.get_environment_log_path_for(an_input)

                # then
                self.assertEqual(expected_result, result)

    def test_get_report_path_at_server_for_dev(self):
        # given
        config_service.settings['mode'] = 'dev'
        expected_result = "d:\\denva\\data\\reports\\"

        # when
        result = config_service.get_report_path_at_server()

        # then
        self.assertEqual(expected_result, result)

        # after
        config_service.set_mode_to('dev')

    def test_get_report_path_at_server_for_server(self):
        # given
        config_service.settings['mode'] = 'server'
        expected_result = "e:\\denva\\data\\reports\\"

        # when
        result = config_service.get_report_path_at_server()

        # then
        self.assertEqual(expected_result, result)

        # after
        config_service.set_mode_to('dev')

    def test_get_default_brightness_for_delight_display_is_in_range(self):
        # when
        result = config_service.get_default_brightness_for_delight_display()

        # then
        self.assertGreaterEqual(result, 0.1)
        self.assertLessEqual(result, 1)

    def test_get_sky_camera_settings(self):
        # when
        result = config_service.is_sky_camera_on()

        # then
        self.assertTrue(isinstance(result, bool))

        # debug
        print(result)

    def test_get_cctv_camera_settings(self):
        # when
        result = config_service.is_cctv_camera_on()

        # then
        self.assertTrue(isinstance(result, bool))

        # debug
        print(result)
