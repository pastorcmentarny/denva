import json
import logging
from datetime import datetime
from retrying import retry

import config
from gateways import web_data_gateway
from pathlib import Path

# TODO MOVE TO CONFIG
STOP_MAX_ATTEMPT_NUMBER = 5
MAXIMUM_WAIT_TIME = 500
MINIMUM_WAIT_TIME = 100

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

        tube_line = columns[1].strip().replace("-city", "")
        tube_status = columns[2].strip()

        for a_line in lines:
            if tube_line == a_line:
                if tube_status in stats_counter[a_line]:
                    stats_counter[a_line][tube_status] += 1
                else:
                    print(f'Add {tube_status}')

    return stats_counter


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def save(new_data: list):
    dt = datetime.now()
    try:
        with open(config.get_file_name_for_tube_status_for(dt), config.APPEND_WITH_READ_MODE) as f:
            for item in new_data:
                f.write(f"{item}\n")
    except Exception as exception:
        logger.warning(f"Unable to save tube status data due to {exception}")


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def save_snapshot(report: dict):
    report_file_path = 'snapshot.txt'
    print(f'Saving report to {report_file_path}')
    logger.info(f'Saving report to {report_file_path}')
    with open(report_file_path, config.WRITE_MODE, encoding=config.ENCODING) as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=4)


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def load():
    try:
        file_path = Path(config.get_file_name_for_tube_status_for(datetime.now()))
        if file_path.exists():
            with open(file_path, config.READ_MODE, newline=config.EMPTY) as file_content:
                return file_content.read().splitlines()
        else:
            logger.warning(f"File : {file_path} doesn't exists.")
            return []
    except Exception as exception:
        logger.warning(f"Unable to load file due to {exception}")
        return []


def update():
    result = web_data_gateway.get_tube_statuses_from_url()
    if len(result) > 0 and result[0] != 'Tube data N/A':
        save(result)
    else:
        logger.warning('Unable to save data as they was a problem with getting data from TfL')
    result_snapshot = load()
    problem_counter = count_tube_problems(result_snapshot)
    save_snapshot(problem_counter)


@retry(wait_random_min=MINIMUM_WAIT_TIME, wait_random_max=MAXIMUM_WAIT_TIME,
       stop_max_attempt_number=STOP_MAX_ATTEMPT_NUMBER)
def load_for(dt):
    try:
        with open(config.get_spectrometer_data_for_date(dt), config.READ_MODE, newline=config.READ_MODE) as file_content:
            return file_content.read().splitlines()
    except Exception as exception:
        logger.warning(f'Unable to load file due to {exception}')


def get_counter_for(date: datetime):
    result = {'tube': count_tube_problems(load_for(date))}
    print(result)
    logger.info(result)
    return result
