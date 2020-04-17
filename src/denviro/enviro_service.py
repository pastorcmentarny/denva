from reports import averages, records, report_service
import commands
import sensor_log_reader
import sensor_warnings


# TODO refactor name
def get_current_measurement(host: str) -> dict:
    measurement = sensor_log_reader.get_last_enviro_measurement()
    measurement['host'] = host
    measurement['system'] = commands.get_system_info()
    return measurement



def get_report_for_yesterday():
    return report_service.generate_enviro_report_for_yesterday()


def get_averages_for_today():
    return averages.get_enviro_averages_for_today()


def get_last_measurement():
    return sensor_log_reader.get_last_enviro_measurement()


def get_records_for_today():
    return records.get_enviro_records_for_today()


def get_current_warnings():
    return sensor_warnings.get_current_warnings_for_enviro()


def get_current_warnings_count():
    return sensor_warnings.count_warning_today()  # TODO is it right call ?
