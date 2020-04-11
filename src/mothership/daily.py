from pathlib import Path

from _datetime import datetime
import utils

path = Path(__file__).parent / '../data/routine_daily.txt'

def load_routine() -> list:
    timetable = []
    file = open(path, 'r', encoding="UTF-8", newline='')
    content = file.readlines()
    for line in content:
        timetable.append(line.rstrip())
    return timetable

def get_now_and_next_event(current_time: int) -> list:
    routine = load_routine()
    for event in routine:
        event_in_minutes = utils.convert_time_to_minutes(event)
        if current_time <= event_in_minutes:
            idx = routine.index(event)
            return [routine[idx - 1], routine[idx]]

    return [routine[len(routine) - 1], routine[0]]



if __name__ == '__main__':
    print(get_now_and_next_event(datetime.now().hour * 60 + datetime.now().minute))
