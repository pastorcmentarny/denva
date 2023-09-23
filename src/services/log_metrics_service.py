import copy

DEBUG = 'DEBUG'
INFO = 'INFO'
WARNING = 'WARNING'
CRITICAL = 'CRITICAL'
ERROR = 'ERROR'
ENCODING = 'UTF-8'
TOTAL_COUNT = 'total_count'


def load_logs(path):
    with open(path, 'r', encoding=ENCODING) as logs_file:
        return logs_file.read().splitlines()


log_metrics = {
    CRITICAL: 0,
    ERROR: 0,
    WARNING: 0,
    INFO: 0,
    DEBUG: 0,
    TOTAL_COUNT: 0
}


def get_total_count_of_log() -> int:
    return log_metrics[CRITICAL] + log_metrics[ERROR] + log_metrics[WARNING] + log_metrics[INFO] + log_metrics[DEBUG]


def get_stats_for(log_type) -> str:
    if get_total_count_of_log() == 0:
        return "no logs"
    else:
        return f'{log_type.lower()} count: {log_metrics[log_type]} which is {"%.2f" % (log_metrics[log_type] / get_total_count_of_log() * 100)}% of all logs.'


def shows_stats_for_log_metrics():
    all_log_types = [CRITICAL, ERROR, WARNING, INFO, DEBUG]
    for log_type in all_log_types:
        print(get_stats_for(log_type))


def generate_log_stats(path: str):
    log_data = load_logs(path)
    for row in log_data:

        if ' - CRITICAL - ' in row:
            log_metrics[CRITICAL] = log_metrics[CRITICAL] + 1
        elif ' - ERROR - ' in row:
            log_metrics[ERROR] = log_metrics[ERROR] + 1
        elif ' - WARNING - ' in row:
            log_metrics[WARNING] = log_metrics[WARNING] + 1
        elif ' - INFO - ' in row:
            log_metrics[INFO] = log_metrics[INFO] + 1
        elif ' - DEBUG - ' in row:
            log_metrics[DEBUG] = log_metrics[DEBUG] + 1

    log_metrics[TOTAL_COUNT] = get_total_count_of_log()
    return shows_stats_for_log_metrics()


def generate_log_stats_for_knyszogar(path: str):
    log_data = load_logs(path)
    for row in log_data:

        if 'CRITICAL :: ' in row:
            log_metrics[CRITICAL] = log_metrics[CRITICAL] + 1
        elif 'ERROR :: ' in row:
            log_metrics[ERROR] = log_metrics[ERROR] + 1
        elif 'WARNING :: ' in row:
            log_metrics[WARNING] = log_metrics[WARNING] + 1
        elif 'INFO :: ' in row:
            log_metrics[INFO] = log_metrics[INFO] + 1
        elif 'DEBUG :: ' in row:
            log_metrics[DEBUG] = log_metrics[DEBUG] + 1

    log_metrics[TOTAL_COUNT] = get_total_count_of_log()
    return shows_stats_for_log_metrics()


def get_log_metrics() -> dict:
    return copy.deepcopy(log_metrics)


def get_current_log_metrics_for(path: str):
    clear()
    generate_log_stats(path)
    return get_log_metrics()


def get_current_knyszogar_log_metrics_for(path: str):
    clear()
    generate_log_stats_for_knyszogar(path)
    return get_log_metrics()


def clear():
    log_metrics[CRITICAL] = 0
    log_metrics[ERROR] = 0
    log_metrics[WARNING] = 0
    log_metrics[INFO] = 0
    log_metrics[DEBUG] = 0
    log_metrics[TOTAL_COUNT] = 0
