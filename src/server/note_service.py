import logging

import config

logger = logging.getLogger('app')

error_messages = []
ok_messages = []


def get_ok_messages():
    ok_messages_list = ok_messages.copy()
    ok_messages.clear()
    return ok_messages_list


def get_error_messages():
    error_message_list = error_messages.copy()
    error_messages.clear()
    return error_message_list


#TODO move to data_writer
def store_data(content_data: str, filename: str):
    file_path = config.get_path_for_note(filename)
    try:
        with open(file_path, config.WRITE_MODE, newline=config.EMPTY, encoding=config.ENCODING) as report_file:
            report_file.write(content_data)
        ok_messages.append(f'Data saved to {file_path}')
    except IOError as io_exception:
        print(io_exception)
        error_messages.append(f'Unable to save file due to {io_exception}')
        # logger.error(io_exception, exc_info=True)
