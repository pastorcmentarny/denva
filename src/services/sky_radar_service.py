from ddd import aircraft_storage, aircraft_stats


def get_flights_for_today() -> dict:
    return get_flights_for(aircraft_storage.load_processed_data())


def get_flights_for_yesterday():
    return get_flights_for(aircraft_storage.load_processed_for_yesterday())


def get_flights_for(data):
    return {
        'detected': aircraft_stats.count_aircraft_found(data),
        'flights': aircraft_stats.get_flights_found(data),
        'stats': aircraft_stats.get_stats(data)
    }
