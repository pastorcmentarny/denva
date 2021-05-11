import logging
from common import data_files
logger = logging.getLogger('app')


def get_text_to_display():
    return data_files.load_text_to_display()