result_as_dict = {'date': '30.3.2020', 'id': 1, 'lap': 1, 'time': '30.53.1', 'time_in_ds': 18531, 'distance': 260}

result_as_line_in_file = '1;;30.3.2020;;1;;30.53.1;;18531;;260'

result_as_request = '30.53.1--30.3.2020--1--260'


def get_result_with_id(result_id: int,lap:int):
    return {
        'date': '1.1.2068',
        'time': '59.59.9',
        'time_in_ds': 35999,
        'lap': lap,
        'id': result_id
    }
