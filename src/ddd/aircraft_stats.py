#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""


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


def get_stats(aircraft_data) -> dict:
    highest_flight = 0
    highest_flight_flights = []
    fastest_flight = 0
    fastest_flight_flights = []
    if aircraft_data:
        for aircraft_row in aircraft_data:
            if int(aircraft_row[7]) > highest_flight:
                highest_flight = int(aircraft_row[7])
                highest_flight_flights = [aircraft_row[3]]
            elif int(aircraft_row[7]) == highest_flight:
                highest_flight_flights.append(aircraft_row[3])

            if int(aircraft_row[11]) > fastest_flight:
                fastest_flight = int(aircraft_row[11])
                fastest_flight_flights = [aircraft_row[3]]
            elif int(aircraft_row[11]) == fastest_flight:
                fastest_flight_flights.append(aircraft_row[3])
        # remove duplicate
        highest_flight_flights = list(set(highest_flight_flights))
        fastest_flight_flights = list(set(fastest_flight_flights))
    return {'highest': {
        'flight': highest_flight_flights,
        'altitude': highest_flight},
        'fastest': {
            'flight': fastest_flight_flights,
            'speed': fastest_flight}
    }


