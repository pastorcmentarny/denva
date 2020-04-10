import re
from gobshite_exception import GobshiteException


# i use decisecond as small unit for measure time for this run
def to_deciseconds(time: str) -> int:
    if not is_valid_time(time):
        raise GobshiteException
    result = time.split('.')
    print(result)
    if len(result) == 1:
        return int(time) * 10
    if len(result) == 2:
        return int(result[0]) * 10 + int(result[1])
    if len(result) == 3:
        return int(result[0]) * 600 + int(result[1]) * 10 + int(result[2])
    return 0


def is_valid_time(time: str) -> bool:
    if not time or time.isspace():
        return False
    if '-' in time:
        return False
    if bool(re.search('[a-zA-Z,]', time)):
        return False
    result = time.split('.')
    if len(result) > 3:
        return False
    if len(result) == 2 and int(result[0]) >= 60:
        return False
    if len(result) == 3 and int(result[1]) >= 60:
        return False
    return bool(re.findall('[0-9.]', time))


def convert_lap_result_request_to_dict(lap_result: str, result_id: int) -> dict:
    result = lap_result.split('--')
    return {
        'date': result[1],
        'time': result[0],
        'time_in_ds': to_deciseconds(result[0]),
        'lap': int(result[2]),
        'id': result_id
    }


def convert_result_to_line(result: dict) -> str:
    return '{};;{};;{};;{};;{}'.format(result['id'], result['date'], result['lap'], result['time'],
                                       result['time_in_ds'])


def convert_results_to_list_of_string(results: list) -> list:
    result_list = []
    for result in results:
        result_list.append(convert_result_to_line(result))
    return result_list


def convert_line_to_result(line: str) -> dict:
    result_as_list = line.split(';;')
    return {
        'date': result_as_list[1],
        'time': result_as_list[3],
        'time_in_ds': int(result_as_list[4]),
        'lap': int(result_as_list[2]),
        'id': int(result_as_list[0])
    }
