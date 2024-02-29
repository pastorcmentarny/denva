import logging

import config
from common import data_writer

logger = logging.getLogger('app')


def save_denva_measurement(data):
    data_writer.save_dict_data_as_json(config.get_denva_one_data_on_server(), data)


def save_denva_two_measurement(data):
    data_writer.save_dict_data_as_json(config.get_denva_two_data_on_server(), data)
