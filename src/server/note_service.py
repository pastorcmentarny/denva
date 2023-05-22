import logging

logger = logging.getLogger('app')
NEW_LINE = '\n'
EMPTY = ''
READ = 'r'
ENCODING = 'utf-8'
UNKNOWN = '?'
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


def store_data(content_data: str, filename: str):
    file_path = f"/home/pi/data/notes/{filename}.txt"
    try:
        with open(file_path, 'w', newline=EMPTY, encoding=ENCODING) as report_file:
            report_file.write(content_data)
        ok_messages.append(f'Data saved to {file_path}')
    except IOError as io_exception:
        print(io_exception)
        error_messages.append(f'Unable to save file due to {io_exception}')
        # logger.error(io_exception, exc_info=True)
