import gc

import commands
import config_serivce
import networkcheck
import sensor_log_reader
import system_data_service


def run_gc() -> dict:
    result = {
        'memory_before': system_data_service.get_memory_available_in_mb(),
        'memory_after' : '',
        'memory_saved' : ''
    }

    gc.collect()

    result['memory_after'] = system_data_service.get_memory_available_in_mb()
    result['memory_saved'] = int(result['memory_before']) - int(result['memory_after'])
    return result


def get_current_measurement(host:str):
    measurement = sensor_log_reader.get_last_enviro_measurement()
    measurement['host'] = host
    measurement['system'] = commands.get_system_info()
    return measurement


def get_healthcheck(app_name):
    return {"status": "UP",
            "app": app_name,
            "network": networkcheck.network_check(config_serivce.get_options()['inChina'])}


def get_log_app(number:int):
    return commands.get_lines_from_path(config_serivce.get_log_path_for('log_app'), number)


def get_log_hc(number:int):
    return commands.get_lines_from_path(config_serivce.get_log_path_for('log_hc'), number)


def get_log_ui(number:int):
    return commands.get_lines_from_path(config_serivce.get_log_path_for('log_ui'), number)