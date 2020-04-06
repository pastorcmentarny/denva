import gc
import psutil
from _datetime import datetime

import config_service
import utils


def get_boot_time() -> str:
    return datetime.fromtimestamp(psutil.boot_time()).strftime("%d-%m'%Y @ %H:%M:%S")


def get_system_disk_space_free():
    return utils.convert_bytes_to_megabytes(psutil.disk_usage(config_service.get_system_drive()).free)


# add disk free
def get_system_information() -> dict:
    return {
        "CPU Speed": '{} MHz'.format(psutil.cpu_freq().current),
        "Memory Available": get_memory_available_in_mb(),
        "Disk Free": "{} MB".format(get_system_disk_space_free()),
        "Uptime": get_boot_time()
    }


def get_memory_available_in_mb() -> str:
    return '{}MB'.format(utils.convert_bytes_to_megabytes(psutil.virtual_memory().available))


# TODO use this for all services not only server
def get_system_warnings() -> list:
    problems = []
    memory_data = psutil.virtual_memory()
    memory_threshold = config_service.get_memory_available_threshold()
    if memory_data.available <= memory_threshold:
        problems.append('Memory available is low. Memory left: {} bytes.'.format(memory_data.available))
    if get_system_disk_space_free() <= config_service.get_disk_space_available_threshold():
        problems.append('Disk free space is low. Free space left: {} MB.'.format(get_system_disk_space_free()))
    return problems


def run_gc():
    result = {
        'memory_before': get_memory_available_in_mb(),
        'memory_after' : '',
        'memory_saved' : ''
    }

    gc.collect()

    result['memory_after'] = get_memory_available_in_mb()
    result['memory_saved'] = utils.get_int_number_from_text(result['memory_before']) - utils.get_int_number_from_text(result['memory_after'])
    return result

if __name__ == '__main__':
    print(get_system_information())
    print(get_system_warnings())
