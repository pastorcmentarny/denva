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
                             ('server', 'app', 'd:\denva\src\configs\server_log_app_config.json'),
                             ('server', 'ui', 'd:\denva\src\configs\server_log_ui_config.json'),
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
        expected_result = "d:\\denva\\data\\reports\\"

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

    def test_get_system_hc_for_dev(self):
        # given
        expected_result = f'D:\denva\data\hc.json'
        # when
        result = config_service.get_system_hc()

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)

    def test_get_system_hc_for_server(self):
        # given
        config_service.settings['mode'] = 'server'
        expected_result = f'\home\pi\data\hc.json'
        # when
        result = config_service.get_system_hc()

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)

        # after
        config_service.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config_service.get_mode(), 'dev')

    def test_get_directory_path_for_aircraft_dev(self):
        # given
        expected_result = f'D:\denva\data'
        # when
        result = config_service.get_directory_path_for_aircraft()

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)

    def test_get_directory_path_for_aircraft_server(self):
        # given
        config_service.settings['mode'] = 'server'
        expected_result = f'/home/pi/data'
        # when
        result = config_service.get_directory_path_for_aircraft()

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)

        # after
        config_service.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config_service.get_mode(), 'dev')

    def test_get_overseer_mode_file_path(self):
        # given
        expected_result = f'D:\overseer_mode.txt'
        # when
        result = config_service.get_overseer_mode_file_path()

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)

    def test_max_latency_fast(self):
        # given
        expected_result = 200

        # when
        result = config_service.max_latency()

        # then
        self.assertEqual(result, expected_result)

    def test_max_latency_slow(self):
        # given
        expected_result = 1000

        # when
        result = config_service.max_latency(False)

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)

    def test_get_url_for_dump1090(self):
        # given
        expected_result = f'http://192.168.0.201:16601/data.json'

        # when
        result = config_service.get_url_for_dump1090()

        # then
        self.assertEqual(result, expected_result)

        # debug
        print(result)
