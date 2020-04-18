from unittest import TestCase

from services import error_detector_service


class Test(TestCase):
    def test_get_errors_should_return_error_with_low_ram_for_server(self):
        # given
        data = {
            'system': {
                'server': {
                    'Memory Available': '240MB',
                    'Disk Free': '999MB'
                },
                'denva': {
                    'Memory Available': '999MB',
                    'Free Space': '999MB',
                    'Data Free Space': '999MB'
                },
                'enviro': {
                    'Memory Available': '999MB',
                    'Free Space': '64MB',
                    'Data Free Space': '999MB'
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
        result = error_detector_service.get_errors(data)

        # then
        self.assertEqual(len(result), 3)
        self.assertEqual(expected_result, result)
