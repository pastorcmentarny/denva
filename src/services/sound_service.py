import dom_utils
from common import data_files
from retrying import retry
from datetime import datetime


def __retry_on_exception(exception):
    return isinstance(exception, Exception)


@retry(retry_on_exception=__retry_on_exception, wait_exponential_multiplier=50, wait_exponential_max=1000,
       stop_max_attempt_number=5)
def get_last_measurement():
    return data_files.load_json_data_as_dict_from('/home/ds/data/barometric-last-measurement.txt')


def get_diff_between(first_value, second_value):
    return f'{(second_value - first_value):0.3f}'


def get_description_for_noise_level(value):
    if value > 0.61:
        return 'NOISE ALERT'
    elif value > 0.12:
        return 'NOISE WARNING'
    elif value > 0.012:
        return 'NOISE CAUTION'
    elif value > 0.001:
        return 'NOISE DETECTED'
    return 'NO NOISE'


def get_report(data: dict):
    return {
        'timestamp': str(datetime.now()),
        'counter': data['counter'],
        'rms': data['rms'],
        'min_rms': data['rms_min'],
        'max_rms': data['rms_max'],
        'noise_detected': data['noise_low'],
        'noise_detected_description': get_description_for_noise_level(data['noise_low']),
        'noise_detected_percentage': dom_utils.percentage(data['noise_low'], data['counter']),
        'noise_caution': data['noise_caution'],
        'noise_caution_description': get_description_for_noise_level(data['noise_caution']),
        'noise_caution_percentage': dom_utils.percentage(data['noise_caution'], data['counter']),
        'noise_warn': data['noise_warn'],
        'noise_warn_description': get_description_for_noise_level(data['noise_warn']),
        'noise_warn_percentage': dom_utils.percentage(data['noise_warn'], data['counter']),
        'noise_error': data['noise_error'],
        'noise_error_description': get_description_for_noise_level(data['noise_error']),
        'noise_error_percentage': dom_utils.percentage(data['noise_low'], data['counter']),
        'avg10': data['avg10'],
        'avg10_description': get_description_for_noise_level(data['avg10']),
        'avg10_diff': get_diff_between(data['avg10'], data['prev_avg10']),
        'avg100': data['avg100'],
        'avg100_description': get_description_for_noise_level(data['avg100']),
        'avg100_diff': get_diff_between(data['avg100'], data['prev_avg100']),
        'avg600': data['avg600'],
        'avg600_description': get_description_for_noise_level(data['avg600']),
        'avg600_diff': get_diff_between(data['avg600'], data['prev_avg600']),
    }
