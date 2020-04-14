result_as_dict = {'date': '1.4.2020', 'id': 3, 'lap': 1, 'time': '24.46.3', 'time_in_ds': 14863, 'distance': 260}

result_as_line_in_file = '3;;1.4.2020;;1;;24.46.3;;14863;;260'

result_as_request = '24.46.3--1.4.2020--1--260'
last_result_as_request = '59.59.9--1.1.2068--1--260'


def get_result_with_id(result_id: int, lap: int):
    return {
        'date': '1.1.2068',
        'time': '59.59.9',
        'time_in_ds': 35999,
        'lap': lap,
        'id': result_id,
        'distance': 260
    }
