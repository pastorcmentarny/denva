def generate_error_email_data(device, message, exception) -> dict:
    return generate_email_data(device, 'ERROR', f'There was technical disturbance with {device}', message,
                               exception_data=exception)


def generate_ip_email_data(device: str, ip: str) -> dict:
    return generate_email_data(device, 'IP', f'An IP information for starting application',
                               f'An IP for {device} is {ip}.')


def generate_email_data(device: str, email_type: str, subject: str, message: str, exception_data: str = "") -> dict:
    return {
        "device": device,
        "email_type": email_type,
        "subject": subject,
        "message": message,
        "exception": exception_data
    }
