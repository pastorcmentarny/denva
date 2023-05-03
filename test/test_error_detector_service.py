from unittest import TestCase

import config
from services import error_detector_service


class ErrorDetectorServiceTestCases(TestCase):
    def test_get_errors_should_return_error_with_low_ram_for_server(self):
        # given
        data = {
            config.FIELD_SYSTEM: {
                'server': {
                    'Memory Available': '240MB',
                    'Disk Free': '999MB'
                },
                'denva': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',
                },
                'enviro': {
                    'Memory Available': '999MB',
                    'Free Space': '64MB',
                },
                'delight': {
                    'Memory Available': '128MB',
                    'Free Space': '64MB'
                },
            }
        }

        expected_result = ['Memory available on SERVER is VERY LOW.', 'Free space on disk  ON ENVIRO is VERY LOW.',
                           'Free space on disk  ON DELIGHT is VERY LOW.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 3)
        self.assertEqual(expected_result, result)

    def test_bug_0001(self):
        """KeyError: 'Memory Available' due to data not populated"""

        # given
        data = {
            config.FIELD_SYSTEM: {
                'server': {
                    'Memory Available': '999MB',
                    'Disk Free': '999MB'
                },
                'denva': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',
                },
                'enviro': {
                    'Free Space': '999MB',
                },
                'delight': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB'
                },
            }
        }

        expected_result = ['Enviro data is missing.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)

    def test_get_error_for_no_data(self):
        # given
        data = {}

        expected_result = ['No data.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)

    def test_get_error_for_missing_server(self):
        # given
        data = {
            config.FIELD_SYSTEM: {
                'server': {},
                'denva': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',

                },
                'enviro': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',

                },
                'delight': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB'
                },
            }
        }

        expected_result = ['Server data is missing.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)

    def test_get_error_for_missing_denva(self):
        # given
        data = {
            config.FIELD_SYSTEM: {
                'server': {
                    'Memory Available': '999MB',
                    'Disk Free': '999MB'
                },
                'denva': {},
                'enviro': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',

                },
                'delight': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB'
                },
            }
        }

        expected_result = ['Denva data is missing.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)

    def test_get_error_for_missing_enviro(self):
        # given
        data = {
            config.FIELD_SYSTEM: {
                'server': {
                    'Memory Available': '999MB',
                    'Disk Free': '999MB'
                },
                'denva': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',

                },
                'enviro': {},
                'delight': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB'
                },
            }
        }

        expected_result = ['Enviro data is missing.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)

    def test_get_error_for_missing_delight(self):
        # given
        data = {
            config.FIELD_SYSTEM: {
                'server': {
                    'Memory Available': '999MB',
                    'Disk Free': '999MB'
                },
                'denva': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',

                },
                'enviro': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',

                },
                'delight': {},
            }
        }

        expected_result = ['Delight data is missing.']
        # when
        result = error_detector_service.get_errors_from_data(data)

        # then
        self.assertEqual(len(result), 1)
        self.assertEqual(expected_result, result)
