# i use decisecond as small unit for measure time for this run
def to_deciseconds(time: str) -> int:
    # TODO add validator
    result = time.split('.')
    print(result)
    if len(result) == 1:
        return int(time) * 10
    if len(result) == 2:
        return int(result[0]) * 10 + int(result[1])
    if len(result) == 3:
        return int(result[0]) * 600 + int(result[1]) * 10 + int(result[2])
    return 0
