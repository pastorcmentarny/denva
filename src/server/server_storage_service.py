import json

MODE = 'w'
ENCODING = 'utf-8'


def save_denva_measurement(data):
    __save(data, '/home/pi/data/denva_data.json')


def save_denviro_measurement(data):
    __save(data, '/home/pi/data/denviro_data.json')


def save_trases_measurement(data):
    __save(data, '/home/pi/data/trases_data.json')


def __save(data, path):
    with open(path, MODE, encoding=ENCODING) as trases_measurement_file:
        json.dump(data, trases_measurement_file, ensure_ascii=False, indent=4)
