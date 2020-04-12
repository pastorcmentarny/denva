import gobshite_exception

def calculate_score(time:int,distance:int,forgot_to_lap:bool=False) -> int:
    if forgot_to_lap:
        return time+300
    print(distance)

    if 261 >= distance >= 259:
        print('in range {}'.format(distance))
        return time

    if distance < 259:
        print(str((260-distance)*(time/260)))
        return time + ((260-distance)*(260-distance)) + int((260-distance)*(time/260))

    if distance > 261:
        return time-(distance-260)

    raise gobshite_exception.GobshiteException

