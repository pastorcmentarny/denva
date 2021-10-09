import platform

from services import system_data_service, common_service

line = '=' * 20


def display_info():
    print('DEVICE INFORMATION:\n' + line)
    print(f'Node: {platform.node()}')
    print(f'OS: {platform.platform()}')
    print(f'Python: {platform.python_version()}')
    print(f'Processor: {platform.processor()}')
    print(line)
    # move this to common
    if platform.system() == 'Windows':
        print(str(system_data_service.get_system_information()))
    else:
        print(str(common_service.get_system_info()))
    print(line)


if __name__ == '__main__':
    display_info()
