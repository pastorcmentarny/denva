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
