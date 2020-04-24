from denva import denva_sensors_service


def get_all_stats_for_today():
    return denva_sensors_service.load_data_for_today()
