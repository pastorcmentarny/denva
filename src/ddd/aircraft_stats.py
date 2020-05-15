def count_aircraft_found(aircraft_data) -> int:
    if aircraft_data:
        flights = []
        for aircraft_row in aircraft_data:
            if len(aircraft_row) > 3:
                flights.append(aircraft_row[3])
        flights = set(flights)
        flights = list(flights)
        return len(flights)
    return 0


def get_flights_found(aircraft_data) -> list:
    if aircraft_data:
        flights = []
        for aircraft_row in aircraft_data:
            if len(aircraft_row) > 3:
                flights.append(aircraft_row[3])
        flights = set(flights)
        flights = list(flights)
        return flights
    return []
