from ddd import aircraft_storage, aircraft_stats

def get_flights_for_today() -> dict:
    data = aircraft_storage.load_processed_data()
    return {
        'detected': aircraft_stats.count_aircraft_found(data),
        'flights': aircraft_stats.get_flights_found(data),
        'stats': aircraft_stats.get_stats(data)
    }


def get_flights_for_yesterday():
    data = aircraft_storage.load_processed_for_yesterday()
    return {
        'detected': aircraft_stats.count_aircraft_found(data),
        'flights': aircraft_stats.get_flights_found(data),
        'stats': aircraft_stats.get_stats(data)
    }