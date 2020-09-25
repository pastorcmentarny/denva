import config_service
from common import commands
from services import system_data_service


def run_gc() -> dict:
    return system_data_service.run_gc()


def get_healthcheck(app_name: str) -> dict:
    return {"status": "UP",
            "app": app_name}


def get_log_app(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_app'), number)


def get_log_hc(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_hc'), number)


def get_log_ui(number: int):
    return commands.get_lines_from_path(config_service.get_log_path_for('log_ui'), number)


def get_system_info():
    return commands.get_system_info()


def reboot_device():
    return commands.reboot('Requested by UI')


def stop_device(app_name: str):
    return commands.halt(app_name)