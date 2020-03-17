import psutil
from _datetime import datetime

import config_serivce
import utils


def get_boot_time() -> str:
    return datetime.fromtimestamp(psutil.boot_time()).strftime("%d-%m'%Y @ %H:%M:%S")


def get_system_disk_space_free():
    return utils.convert_bytes_to_MB(psutil.disk_usage(config_serivce.get_system_drive()).free)


# add disk free
def get_system_information() -> dict:
    return {
        "CPU freq": psutil.cpu_freq().current,
        "Memory": utils.convert_bytes_to_MB(psutil.virtual_memory().available),
        "Disk Free": get_system_disk_space_free(),
        "Boot Time": get_boot_time()

    }


def get_system_warnings() -> list:
    problems = []
    memory_data = psutil.virtual_memory()
    threshold = config_serivce.get_memory_available_threshold()
    if memory_data.available <= threshold:
        problems.append('Memory available is low. Memory left: {} bytes'.format(memory_data.available))
    return problems


if __name__ == '__main__':
    print(get_system_information())
    print(get_system_warnings())
