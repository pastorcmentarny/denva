import gobshite_exception

NORMAL_DISTANCE = 260


def calculate_score(time: int, distance: int) -> int:

    if distance == 0:
        return time + 450  # move to config?

    if 261 >= distance >= 259:
        return time

    if distance < 259:
        print(str((NORMAL_DISTANCE - distance) * (time / NORMAL_DISTANCE)))
        return time + ((NORMAL_DISTANCE - distance) * (NORMAL_DISTANCE - distance)) + int(
            (NORMAL_DISTANCE - distance) * (time / NORMAL_DISTANCE))

    if distance > 261:
        return time - (distance - NORMAL_DISTANCE)

    raise gobshite_exception.GobshiteException
