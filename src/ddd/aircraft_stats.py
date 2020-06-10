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

    return {'highest': {
        'flight': highest_flight_flights,
        'altitude': highest_flight},
        'fastest': {
            'flight': fastest_flight_flights,
            'speed': fastest_flight}
    }


if __name__ == '__main__':
    aircraft_data_example = [
        '2020-06-05 23:22:44.787250,780747,5212,CSN8082,51.596283,-0.535435,1,8975,2048,72,1,301,96,0'.split(','),
        '2020-06-05 23:23:01.849110,780747,5212,CSN8082,51.603481,-0.502243,1,9550,1856,70,1,309,215,0'.split(','),
        '2020-06-05 23:23:16.669094,780747,5212,CSN8082,51.611163,-0.466309,1,10125,2752,71,1,316,329,0'.split(','),
        '2020-06-05 23:23:32.296789,780747,5212,CSN8082,51.617661,-0.433069,1,10650,1088,73,1,324,422,0'.split(','),
        '2020-06-05 23:23:48.414877,780747,5212,CSN8082,51.625175,-0.39238,1,11050,2112,73,1,336,487,0'.split(','),
        '2020-06-05 23:24:03.655738,780747,5212,CSN8082,51.629608,-0.367968,1,11675,2240,73,1,340,538,0'.split(','),
        '2020-06-05 23:24:20.450910,780747,5212,CSN8082,51.632996,-0.349039,1,11950,1984,73,1,343,568,6'.split(','),
        '2020-06-05 23:24:37.537440,780747,5212,CSN8082,51.644913,-0.283051,1,12825,2240,73,1,352,618,0'.split(','),
        '2020-06-05 23:24:52.872789,780747,5212,CSN8082,51.653641,-0.234944,1,13375,2112,73,1,356,728,0'.split(','),
        '2020-06-05 23:25:09.140006,780747,5212,CSN8082,51.662292,-0.187361,1,13975,2176,73,1,361,825,0'.split(','),
        '2020-06-05 23:25:27.081463,780747,5212,CSN8082,51.668472,-0.153363,1,14500,2048,73,1,365,917,0'.split(','),
        '2020-06-05 23:25:41.173099,780747,5212,CSN8082,51.675064,-0.117212,1,14900,2048,73,1,369,972,2'.split(','),
        '2020-06-05 23:25:58.372146,780747,5212,CSN8082,51.675064,-0.117212,1,14900,2048,73,1,369,973,14'.split(','),
        '2020-06-05 23:30:30.379383,780747,5212,CSN8082,51.675064,-0.117212,1,14900,2048,73,1,369,973,287'.split(','),
        '2020-06-05 23:30:30.379383,780747,5212,UFO1000,51.675064,-0.117212,1,14900,2048,73,1,369,973,287'.split(','),
        '2020-06-05 23:30:30.379383,780747,5212,UFO1011,51.675064,-0.117212,1,14900,2048,73,1,550,973,287'.split(','),
        '2020-06-05 23:30:30.379383,780747,5212,UFO1012,51.675064,-0.117212,1,14900,2048,73,1,550,973,287'.split(','),
        '2020-06-05 23:30:30.379383,780747,5212,CSN8082,51.675064,-0.117212,1,39000,2048,73,1,369,973,287'.split(','),
        '2020-06-05 23:57:19.220115,448465,1172,FRH552,51.565867,-0.259323,1,39000,0,103,1,550,154,1'.split(',')]
    print(get_stats(aircraft_data_example))
