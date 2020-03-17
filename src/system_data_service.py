import config_serivce
import psutil


def get_system_warnings() -> list:
    problems = []
    memory_data = psutil.virtual_memory()
    threshold = config_serivce.get_memory_available_threshold()
    if memory_data.available <= threshold:
        problems.append('Memory available is low. Memory left: {} bytes'.format(memory_data.available))
    return problems

if __name__ == '__main__':
    print(get_system_warnings())