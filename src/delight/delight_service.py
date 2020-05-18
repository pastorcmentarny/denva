import logging

import config_service
from common import commands
from ddd import aircraft_storage, aircraft_stats
from gateways import local_data_gateway
from services import system_data_service

logger = logging.getLogger('app')


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_log_app(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_app'), number)


def get_log_hc(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_hc'), number)


def get_log_ui(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_ui'), number)


def get_system_info():
    return commands.get_system_info()


def get_hc_for_radar():
    response = {
        'dump': 'DOWN',
        'digest': commands.is_dump_digest_active()
    }
    dump_response = local_data_gateway.get_data_for(config_service.get_radar_hc_url(), 2)

    if 'error' in dump_response:
        logger.warning(dump_response['error'])
    else:
        response['dump'] = 'UP'

    return response


def get_flights_for_today() -> dict:
    data = aircraft_storage.load_processed_data()
    return {
        'detected': aircraft_stats.count_aircraft_found(data),
        'flights': aircraft_stats.get_flights_found(data)
    }


def get_flights_for_yesterday():
    data = aircraft_storage.load_processed_for_yesterday()
    return {
        'detected': aircraft_stats.count_aircraft_found(data),
        'flights': aircraft_stats.get_flights_found(data)
    }
