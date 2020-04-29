from denva import denva_sensors_service
from reports import averages, records, report_service
from services import sensor_warnings_service


def get_all_stats_for_today():
    return denva_sensors_service.load_data_for_today()


def get_warnings_for(year, month, day):
    return sensor_warnings_service.get_warnings_for(year, month, day)


def count_warnings():
    return denva_sensors_service.count_warnings(sensor_warnings_service.get_warnings_for_today())


def get_current_warnings():
    return sensor_warnings_service.get_current_warnings()


def get_warnings_for_today():
    return sensor_warnings_service.get_warnings_for_today()


def get_averages():
    return averages.get_averages_for_today()


def get_records_for_today():
    return records.get_records_for_today()


def get_last_measurement_from_sensor():
    return denva_sensors_service.get_last_measurement()


def get_last_report():
    return report_service.generate_for_yesterday()
