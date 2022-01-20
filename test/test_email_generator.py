import unittest

from emails import email_generator


class EmailGeneratorTestCases(unittest.TestCase):

    def test_generate_ip_email_data(self):
        # given
        device = 'device'
        ip = '192.168.0.1'
        expected_result = {
            "device": device,
            "email_type": 'IP',
            "subject": 'An IP information for starting application',
            "message": f'An IP for {device} is {ip}.',
            "exception": ''
        }

        # when
        result = email_generator.generate_ip_email_data(device, ip)

        # debug
        print(f'Result of generating email data is : {result}')

        # then
        self.assertEqual(expected_result, result)

    def test_generate_error_email_data(self):
        # given
        device = 'device'
        exception = 'KAABOOM'
        message = 'whoops'

        expected_result = {
            "device": device,
            "email_type": 'ERROR',
            "subject": 'There was technical disturbance with device',
            "message": message,
            "exception": exception
        }

        # when
        result = email_generator.generate_error_email_data(device, message, exception)

        # debug
        print(f'Result of generating email data is : {result}')

        # then
        self.assertEqual(expected_result, result)

    def test_generate_email_data(self):
        # given
        device = 'device'
        email_type = 'normal'
        subject = 'title'
        message = 'ok'
        expected_result = {
            "device": device,
            "email_type": email_type,
            "subject": subject,
            "message": message,
            "exception": ""
        }

        # when
        result = email_generator.generate_email_data(device, email_type, subject, message)

        # debug
        print(f'Result of generating email data is : {result}')

        # then
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
