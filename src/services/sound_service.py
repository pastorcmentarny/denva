import config
import dom_utils
from common import data_loader

from datetime import datetime


def get_last_measurement():
    return data_loader.load_json_data_as_dict_from('/home/ds/data/sound-last-measurement.txt')


def get_diff_between(first_value, second_value):
    return f'{(second_value - first_value):0.3f}'


# TODO move result message to config
def get_description_for_noise_level(value):
    if value > config.get_noise_alert_level():
        return 'NOISE ALERT'
    elif value > config.get_noise_warning_level():
        return 'NOISE WARNING'
    elif value > config.get_noise_caution_level():
        return 'NOISE CAUTION'
    elif value > config.get_noise_dected_level():
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
