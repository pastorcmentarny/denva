from datetime import datetime
from timeit import default_timer as timer

from common import loggy


def get_all_airplanes() -> dict:
    start_time = timer()
    today = datetime.now()
    path = f"/home/pi/data/{today.year}/{today.month:02d}/{today.day:02d}/aircraft.txt"
    # if os.path.exists(path) if not ,return 'not exists'
    file = open(path, 'r', newline='')
    detected_entries = file.readlines()
    all_aircraft = []
    for row in detected_entries:
        row = row.split(',')
        print(row)
        if row[10] != '':
            all_aircraft.append(row[10].strip())
    result_as_set = set(all_aircraft)
    all_aircraft = (list(result_as_set))
    loggy.log_time('Getting airplane measurement', start_time, timer())
    return {'flights': all_aircraft}
