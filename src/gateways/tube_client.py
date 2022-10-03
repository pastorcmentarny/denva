import json
import logging
from datetime import datetime
from retrying import retry
from gateways import web_data_gateway

STOP_MAX_ATTEMPT_NUMBER = 5
MAXIMUM_WAIT_TIME = 500
MINIMUM_WAIT_TIME = 100

ENCODING = 'utf-8'
TIME_UNIT = 5

logger = logging.getLogger('app')

statuses = []

lines = ['Bakerloo', 'Central', 'Circle', 'District', 'Hammersmith', 'Jubilee', 'Metropolitan', 'Northern',
         'Piccadilly', 'Victoria', 'Waterloo']


def count_tube_problems(problem_list) -> dict:
    stats_counter = {
        'Bakerloo': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,

        },
        'Central': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Circle': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'District': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Hammersmith': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Jubilee': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Metropolitan': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Northern': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Piccadilly': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Victoria': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        },
        'Waterloo': {
            'Good Service': 0,
            'Minor Delays': 0,
            'Severe Delays': 0,
            'Part Suspended': 0,
            'Part Closure': 0,
            'Planned Closure': 0,
            'Reduced Service': 0,
            'Suspended': 0,
            'Service Closed': 0,
        }
    }

    for problem in problem_list:
        columns = problem.split('::')
        timestamp = columns[0]

        tube_line = columns[1].strip().replace("-city", "")
        tube_status = columns[2].strip()

        for a_line in lines:
            if tube_line == a_line:
                if tube_status in stats_counter[a_line]:
                    stats_counter[a_line][tube_status] += 1
                else:
                    print(f'Add {tube_status}')

    return stats_counter


def get_file_name(dt):
    return f"/home/pi/data/tube-status{dt.year}{dt.month:02d}{dt.day:02d}.txt"


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def save(new_data: list):
    dt = datetime.now()
    with open(get_file_name(dt), 'a+') as f:
        for item in new_data:
            f.write(f"{item}\n")


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def save_snapshot(report: dict):
    report_file_path = 'snapshot.txt'
    print('Saving report to {}'.format(report_file_path))
    logger.info('Saving report to {}'.format(report_file_path))
    with open(report_file_path, 'w', encoding=ENCODING) as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=4)


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def load():
    try:
        dt = datetime.now()
        with open(get_file_name(dt), 'r', newline='') as file_content:
            return file_content.read().splitlines()
    except Exception as exception:
        logger.warning(f"Unable to load file due to {exception}")

def update():
    result = web_data_gateway.get_tube_statuses_from_url()
    if len(result) > 0 and result[0] != 'Tube data N/A':
        save(result)
    result_snapshot = load()
    problem_counter = count_tube_problems(result_snapshot)
    save_snapshot(problem_counter)
