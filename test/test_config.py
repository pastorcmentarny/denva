from unittest import TestCase

import config


class ConfigServiceTestCases(TestCase):
    def test_get_irregular_verbs_path(self):
        # given
        config.set_mode_to('dev')

        # when
        result = config.get_irregular_verbs_path()

        # then
        self.assertTrue(result.endswith('data/irregular_verbs.txt'))

    def test_get_shaking_level(self):
        # when
        result = config.get_shaking_level()

        # then
        self.assertEqual(result, 1000)

    def test_set_mode_to(self):
        # when
        config.set_mode_to('server')

        # then
        self.assertEqual(config.get_mode(), 'server')

    def test_get_environment_log_path_for(self):
        # given
        scale_params_list = [('denva', 'app', '/home/ds/configs/log_app_config.json'),
                             ('denva', 'ui', '/home/ds/configs/log_ui_config.json'),
                             ('dev', 'app', '/home/ds/configs/dev_log_app_config.json'),
                             ('dev', 'ui', '/home/ds/configs/dev_log_ui_config.json'),
                             ('server', 'app', '/home/ds/configs/server_log_app_config.json'),
                             ('server', 'ui', '/home/ds/configs/server_log_ui_config.json'),
                             ('dev', 'ddd', '/home/ds/configs/dev_log_ddd_config.json'),
                             ('ddd', 'ddd', '/home/ds/configs/dev_log_ddd_config.json'),
                             ('overseer_mode', 'overseer_mode', '/home/ds/configs/overseer_mode.json'),
                             ('overseer', 'overseer', '/home/ds/configs/overseer.json'),
                             ('hc', 'hc', '/home/ds/configs/log_config.json'),
                             ]

        for mode, an_input, expected_result in scale_params_list:
            with self.subTest(
                    msg=f"Checking to get_environment_log_path_for() for mode {mode} & app type {an_input} "):
                # given
                config.load_cfg()['mode'] = mode
                # when
                result = config.get_environment_log_path_for(an_input)

                # then
                self.assertEqual(expected_result, result)

    def test_get_sky_camera_settings(self):
        # when
        result = config.is_sky_camera_on()

        # then
        self.assertTrue(isinstance(result, bool))

        # debug
        print(result)

    def test_get_cctv_camera_settings(self):
        # when
        result = config.is_cctv_camera_on()

        # then
        self.assertTrue(isinstance(result, bool))

        # debug
        print(result)

    def test_get_system_hc_for_dev(self):
        # given
        expected_result = f'\\home\\pi\\data\\hc.json'
        # when
        result = config.get_system_hc()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_system_hc_for_server(self):
        # given
        config.settings['mode'] = 'server'
        expected_result = f'\home\pi\data\hc.json'
        # when
        result = config.get_system_hc()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

        # after
        config.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config.get_mode(), 'dev')

    def test_get_directory_path_for_aircraft_dev(self):
        # given
        expected_result = f'/home/ds/data/'
        # when
        result = config.get_directory_path_for_aircraft()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_directory_path_for_aircraft_server(self):
        # given
        config.settings['mode'] = 'server'
        expected_result = f'/home/ds/data/'
        # when
        result = config.get_directory_path_for_aircraft()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

        # after
        config.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config.get_mode(), 'dev')

    def test_get_overseer_mode_file_path(self):
        # given
        expected_result = f'/home/ds/overseer_mode.txt'
        # when
        result = config.get_overseer_mode_file_path()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_max_latency_fast(self):
        # given
        expected_result = 200

        # when
        result = config.max_latency()

        # then
        self.assertEqual(expected_result, result)

    def test_max_latency_slow(self):
        # given
        expected_result = 1000

        # when
        result = config.max_latency(False)

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_url_for_dump1090(self):
        # given
        expected_result = f'http://192.168.0.201:16601/data.json'

        # when
        result = config.get_url_for_dump1090()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_radar_hc_url(self):
        # given
        expected_result = f'http://192.168.0.201:5000/hc/ar'

        # when
        result = config.get_radar_hc_url()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_system_hc(self):
        # given
        expected_result = f'\\home\\pi\\data\\hc.json'

        # when
        result = config.get_system_hc()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_service_on_off_url(self):
        # given
        expected_result = f'http://192.168.0.200:5000/shc/change'

        # when
        result = config.get_service_on_off_url()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_warm_up_measurement_counter(self):
        # given
        expected_result = 10

        # when
        result = config.get_warm_up_measurement_counter()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_sensor_log_file_for(self):
        # given
        expected_result = f'/home/ds/logs/sensor-log-2021-01-02.csv'

        # when
        result = config.get_sensor_log_file_for(2021, 1, 2)

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_sensitivity(self):
        # given
        expected_result = 8
        # when
        result = config.get_sensitivity()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_disk_space_available_threshold(self):
        # given
        expected_result = 500

        # when
        result = config.get_disk_space_available_threshold()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_memory_available_threshold(self):
        # given
        expected_result = 262144000

        # when
        result = config.get_memory_available_threshold()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_disk_space_available_threshold(self):
        # given
        expected_result = 500

        # when
        result = config.get_disk_space_available_threshold()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_path_for_data_bin(self):
        # given
        expected_result = 500

        # when
        result = config.get_disk_space_available_threshold()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_metrics_service_url(self):
        # given
        expected_result = f'http://192.168.0.200:5000/metrics/add'

        # when
        result = config.get_metrics_service_url()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_system_hc_reboot_url(self):
        # given
        expected_result = f'http://192.168.0.200:5000/shc/reboot'

        # when
        result = config.get_system_hc_reboot_url()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_path_for_personal_events(self):
        # given
        expected_result = f'/home/ds/events.json'

        # when
        result = config.get_path_for_personal_events()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_options(self):
        # given
        expected_result = {'inChina': False}

        # when
        result = config.get_options()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_current_warnings_url_for(self):
        # given
        expected_result = f'http://192.168.0.200:5000/warns/now'

        # when
        result = config.get_current_warnings_url_for('server')

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_healthcheck_ip(self):
        # given
        expected_result = f'http://192.168.0.200:5000'

        # when
        result = config.get_healthcheck_ip()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_information_path_for_server(self):
        # given
        config.settings['mode'] = 'server'
        expected_result = f'/home/ds/data/information.json'

        # when
        result = config.get_information_path()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

        # after
        config.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config.get_mode(), 'dev')

    def test_get_information_path_for_dev(self):
        # given
        config.settings['mode'] = 'dev'
        expected_result = f'/home/ds/data/information.json'

        # when
        result = config.get_information_path()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

        # after
        config.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config.get_mode(), 'dev')

    def test_get_log_path_for(self):
        # given
        expected_result = f'/home/ds/configs/dev_log_app_config.json'

        # when
        result = config.get_log_path_for('dev_app')

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_path_to_chinese_dictionary_for_dev(self):
        # given
        config.settings['mode'] = 'dev'
        expected_result = f'/home/ds/data/dictionary.txt'

        # when
        result = config.get_path_to_chinese_dictionary()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

        # after
        config.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config.get_mode(), 'dev')

    def test_get_path_to_chinese_dictionary_for_server(self):
        # given
        config.settings['mode'] = 'server'
        expected_result = f'/home/ds/data/dictionary.txt'

        # when
        result = config.get_path_to_chinese_dictionary()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

        # after
        config.settings['mode'] = 'dev'

        # verify
        self.assertEqual(config.get_mode(), 'dev')

    def test_get_system_hc_url(self):
        # given
        expected_result = f'http://192.168.0.200:5000/shc/update'

        # when
        result = config.get_system_hc_url()

        # then
        self.assertEqual(expected_result, result)

        # debug
        print(result)

    def test_get_slow_refresh_rate(self):
        # given
        expected_result = 5

        # when
        result = config.get_slow_refresh_rate()

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_get_normal_refresh_rate(self):
        # given
        expected_result = 1

        # when
        result = config.get_normal_refresh_rate()

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_is_cli_mode_enabled(self):
        # when
        result = config.is_cli_mode_enabled()

        # debug
        print(f'CLI Enabled {result}')

        # then
        self.assertFalse(result)

    def test_get_fast_refresh_rate(self):
        # given
        expected_result = 0.25

        # when
        result = config.get_fast_refresh_rate()

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)

    def test_get_today_warnings(self):
        # given
        expected_result = "/home/ds/data/all-warnings.txt"

        # when
        result = config.get_today_warnings()

        # debug
        print(result)

        # then
        self.assertEqual(expected_result, result)
