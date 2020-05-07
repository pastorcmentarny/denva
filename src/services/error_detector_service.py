import logging
from gateways import local_data_gateway
from common import dom_utils, loggy

logger = logging.getLogger('app')


def get_errors_from_data(data: dict) -> list:
    errors = []
    if 'system' not in data:
        return ['No data.']

    hc_result = local_data_gateway.get_all_healthcheck_from_all_services()
    if hc_result['denva'] == 'DOWN':
        errors.append('Healthcheck failed for Denva')
    if hc_result['enviro'] == 'DOWN':
        errors.append('Healthcheck failed for Denviro')
    if hc_result['server'] == 'DOWN':
        errors.append('Healthcheck failed for Server')
    if hc_result['delight'] == 'DOWN':
        errors.append('Healthcheck failed for Delight')

    server_data = data['system']['server']
    if 'server' in data['system'] and 'Memory Available' in server_data:
        if dom_utils.get_int_number_from_text(server_data['Memory Available']) < 500:
            errors.append('Memory available on SERVER is VERY LOW.')
        if dom_utils.get_int_number_from_text(server_data['Disk Free']) < 128:
            errors.append('Free space on disk  ON SERVER is VERY LOW.')
    else:
        errors.append('Server data is missing.')

    denva_data = data['system']['denva']
    if 'denva' in data['system'] and 'Memory Available' in denva_data:
        if dom_utils.get_int_number_from_text(denva_data['Memory Available']) < 128:
            errors.append('Memory available ON DENVA is VERY LOW.')
        if dom_utils.get_int_number_from_text(denva_data['Free Space']) < 128:
            errors.append('Free space on disk  ON DENVA is VERY LOW.')
        if dom_utils.get_int_number_from_text(denva_data['Data Free Space']) < 256:
            errors.append('Free space on data partition ON DENVA is VERY LOW.')
    else:
        errors.append('Denva data is missing.')

    enviro_data = data['system']['enviro']
    if 'enviro' in data['system'] and 'Memory Available' in enviro_data:
        if dom_utils.get_int_number_from_text(enviro_data['Memory Available']) < 128:
            errors.append('Memory available ON ENVIRO is VERY LOW.')
        if dom_utils.get_int_number_from_text(enviro_data['Free Space']) < 128:
            errors.append('Free space on disk  ON ENVIRO is VERY LOW.')
        if dom_utils.get_int_number_from_text(enviro_data['Data Free Space']) < 256:
            errors.append('Free space on data partition ON ENVIRO is VERY LOW.')
    else:
        errors.append('Enviro data is missing.')

    delight_data = data['system']['delight']
    if 'delight' in data['system'] and 'Memory Available' in delight_data:
        if dom_utils.get_int_number_from_text(delight_data['Memory Available']) < 128:
            errors.append('Memory available ON DELIGHT is VERY LOW.')
        if dom_utils.get_int_number_from_text(delight_data['Free Space']) < 128:
            errors.append('Free space on disk  ON DELIGHT is VERY LOW.')
    else:
        errors.append('Delight data is missing.')
    loggy.log_error_count(errors)
    return errors



