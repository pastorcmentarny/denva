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
import data_files
import utils


def get_stats_file_for(year: str, month: str, day: str) -> list:
    date = utils.get_filename_for_stats(year, month, day)
    return data_files.load_stats('/home/pi/logs/' + date)


def count_tube_color_for(year, month, day) -> dict:
    return count_tube_color(get_stats_file_for(year, month, day))


def get_stats_file_for_today() -> list:
    return data_files.load_stats('/home/pi/logs/stats.log')


def count_tube_color_today() -> dict:
    return count_tube_color(get_stats_file_for_today())


def count_tube_color(stats_list) -> dict:
    stats_counter = {
        'Bakerloo': 0,
        'Central': 0,
        'Circle': 0,
        'District': 0,
        'Hammersmith': 0,
        'Jubilee': 0,
        'Metropolitan': 0,
        'Piccadilly': 0,
        'Victoria': 0,
        'Waterloo': 0
    }

    for stat in stats_list:
        if 'Bakerloo line' in stat:
            stats_counter['Bakerloo'] += 1
        elif 'Central line' in stat:
            stats_counter['Central'] += 1
        elif 'Circle line' in stat:
            stats_counter['Circle'] += 1
        elif 'District line' in stat:
            stats_counter['District'] += 1
        elif 'Hammersmith & City line' in stat:
            stats_counter['Hammersmith'] += 1
        elif 'Jubilee line' in stat:
            stats_counter['Jubilee'] += 1
        elif 'Metropolitan line' in stat:
            stats_counter['Metropolitan'] += 1
        elif 'Piccadilly line' in stat:
            stats_counter['Piccadilly'] += 1
        elif 'Victoria line' in stat:
            stats_counter['Victoria'] += 1
        elif 'Waterloo & City line' in stat:
            stats_counter['Waterloo'] += 1

    return stats_counter


def count_tube_problems_for(year, month, day) -> dict:
    return count_tube_problems(get_stats_file_for(year, month, day))


def count_tube_problems_today() -> dict:
    return count_tube_problems(get_stats_file_for_today())


def count_tube_problems(problem_list) -> dict:
    stats_counter = {
        'BakerlooMD': 0,
        'BakerlooSD': 0,
        'BakerlooPS': 0,
        'BakerlooFS': 0,
        'BakerlooTotalTime': 0,
        'CentralMD': 0,
        'CentralSD': 0,
        'CentralPS': 0,
        'CentralFS': 0,
        'CentralTotalTime': 0,
        'CircleMD': 0,
        'CircleSD': 0,
        'CirclePS': 0,
        'CircleFS': 0,
        'CircleTotalTime': 0,
        'DistrictMD': 0,
        'DistrictSD': 0,
        'DistrictPS': 0,
        'DistrictFS': 0,
        'DistrictTotalTime': 0,
        'HammersmithMD': 0,
        'HammersmithSD': 0,
        'HammersmithPS': 0,
        'HammersmithFS': 0,
        'HammersmithTotalTime': 0,
        'JubileeMD': 0,
        'JubileeSD': 0,
        'JubileePS': 0,
        'JubileeFS': 0,
        'JubileeTotalTime': 0,
        'MetropolitanMD': 0,
        'MetropolitanSD': 0,
        'MetropolitanPS': 0,
        'MetropolitanFS': 0,
        'MetropolitanTotalTime': 0,
        'NorthernMD': 0,
        'NorthernSD': 0,
        'NorthernPS': 0,
        'NorthernFS': 0,
        'NorthernTotalTime': 0,
        'PiccadillyMD': 0,
        'PiccadillySD': 0,
        'PiccadillyPS': 0,
        'PiccadillyFS': 0,
        'PiccadillyTotalTime': 0,
        'VictoriaMD': 0,
        'VictoriaSD': 0,
        'VictoriaPS': 0,
        'VictoriaFS': 0,
        'VictoriaTotalTime': 0,
        'WaterlooMD': 0,
        'WaterlooSD': 0,
        'WaterlooPS': 0,
        'WaterlooFS': 0,
        'WaterlooTotalTime': 0
    }

    for problem in problem_list:
        if 'bakerloo has Minor Delays' in problem:
            stats_counter['BakerlooMD'] += 1
        if 'bakerloo has Severe Delays' in problem:
            stats_counter['BakerlooSD'] += 1
        if 'bakerloo has Part Suspended' in problem:
            stats_counter['BakerlooPS'] += 1
        if 'bakerloo has Suspended' in problem:
            stats_counter['BakerlooFS'] += 1
        if 'central has Minor Delays' in problem:
            stats_counter['CentralMD'] += 1
        if 'central has Severe Delays' in problem:
            stats_counter['CentralSD'] += 1
        if 'central has Part Suspended' in problem:
            stats_counter['CentralPS'] += 1
        if 'central has Suspended' in problem:
            stats_counter['CentralFS'] += 1
        if 'circle has Minor Delays' in problem:
            stats_counter['CentralMD'] += 1
        if 'circle has Severe Delays' in problem:
            stats_counter['CentralSD'] += 1
        if 'circle has Part Suspended' in problem:
            stats_counter['CentralPS'] += 1
        if 'circle has Suspended' in problem:
            stats_counter['CentralFS'] += 1
        if 'district has Minor Delays' in problem:
            stats_counter['DistrictMD'] += 1
        if 'district has Severe Delays' in problem:
            stats_counter['DistrictSD'] += 1
        if 'district has Part Suspended' in problem:
            stats_counter['DistrictPS'] += 1
        if 'district has Suspended' in problem:
            stats_counter['DistrictFS'] += 1
        if 'hammersmith-city has Minor Delays' in problem:
            stats_counter['HammersmithMD'] += 1
        if 'hammersmith-city has Severe Delays' in problem:
            stats_counter['HammersmithSD'] += 1
        if 'hammersmith-city has Part Suspended' in problem:
            stats_counter['HammersmithPS'] += 1
        if 'hammersmith-city has Suspended' in problem:
            stats_counter['HammersmithFS'] += 1
        if 'jubilee has Minor Delays' in problem:
            stats_counter['JubileeMD'] += 1
        if 'jubilee has Severe Delays' in problem:
            stats_counter['JubileeSD'] += 1
        if 'jubilee has Part Suspended' in problem:
            stats_counter['JubileePS'] += 1
        if 'jubilee has Suspended' in problem:
            stats_counter['JubileeFS'] += 1
        if 'metropolitan has Minor Delays' in problem:
            stats_counter['MetropolitanMD'] += 1
        if 'metropolitan has Severe Delays' in problem:
            stats_counter['MetropolitanSD'] += 1
        if 'metropolitan has Part Suspended' in problem:
            stats_counter['MetropolitanPS'] += 1
        if 'metropolitan has Suspended' in problem:
            stats_counter['MetropolitanFS'] += 1
        if 'northern has Minor Delays' in problem:
            stats_counter['NorthernMD'] += 1
        if 'northern has Severe Delays' in problem:
            stats_counter['NorthernSD'] += 1
        if 'northern has Part Suspended' in problem:
            stats_counter['NorthernPS'] += 1
        if 'northern has Suspended' in problem:
            stats_counter['NorthernFS'] += 1
        if 'piccadilly has Minor Delays' in problem:
            stats_counter['PiccadillyMD'] += 1
        if 'piccadilly has Severe Delays' in problem:
            stats_counter['PiccadillySD'] += 1
        if 'piccadilly has Part Suspended' in problem:
            stats_counter['PiccadillyPS'] += 1
        if 'piccadilly has Suspended' in problem:
            stats_counter['PiccadillyFS'] += 1
        if 'victoria has Minor Delays' in problem:
            stats_counter['VictoriaMD'] += 1
        if 'victoria has Severe Delays' in problem:
            stats_counter['VictoriaSD'] += 1
        if 'victoria has Part Suspended' in problem:
            stats_counter['VictoriaPS'] += 1
        if 'victoria has Suspended' in problem:
            stats_counter['VictoriaFS'] += 1
        if 'waterloo-city has Minor Delays' in problem:
            stats_counter['WaterlooMD'] += 1
        if 'waterloo-city has Severe Delays' in problem:
            stats_counter['WaterlooSD'] += 1
        if 'waterloo-city has Part Suspended' in problem:
            stats_counter['WaterlooPS'] += 1
        if 'waterloo-city has Suspended' in problem:
            stats_counter['WaterlooFS'] += 1

        stats_counter['BakerlooTotalTime'] = str((stats_counter['BakerlooMD'] + stats_counter['BakerlooSD'] +
                                                  stats_counter['BakerlooPS'] + stats_counter[
                                                      'BakerlooFS']) * 5) + " seconds."
        stats_counter['CentralTotalTime'] = str((stats_counter['CentralMD'] + stats_counter['CentralSD'] +
                                                 stats_counter['CentralPS'] + stats_counter[
                                                     'CentralFS']) * 5) + " seconds."
        stats_counter['CircleTotalTime'] = str((stats_counter['CircleMD'] + stats_counter['CircleSD'] + stats_counter[
            'CirclePS'] + stats_counter['CircleFS']) * 5) + " seconds."
        stats_counter['DistrictTotalTime'] = str((stats_counter['DistrictMD'] + stats_counter['DistrictSD'] +
                                                  stats_counter['DistrictPS'] + stats_counter[
                                                      'DistrictFS']) * 5) + " seconds."
        stats_counter['HammersmithTotalTime'] = str((stats_counter['HammersmithMD'] + stats_counter['HammersmithSD'] +
                                                     stats_counter['HammersmithPS'] + stats_counter[
                                                         'HammersmithFS']) * 5) + " seconds."
        stats_counter['JubileeTotalTime'] = str((stats_counter['JubileeMD'] + stats_counter['JubileeSD'] +
                                                 stats_counter['JubileePS'] + stats_counter[
                                                     'JubileeFS']) * 5) + " seconds."
        stats_counter['MetropolitanTotalTime'] = str((stats_counter['MetropolitanMD'] + stats_counter[
            'MetropolitanSD'] + stats_counter['MetropolitanPS'] + stats_counter['MetropolitanFS']) * 5) + " seconds."
        stats_counter['NorthernTotalTime'] = str((stats_counter['NorthernMD'] + stats_counter['NorthernSD'] +
                                                  stats_counter['NorthernPS'] + stats_counter[
                                                      'NorthernFS']) * 5) + " seconds."
        stats_counter['PiccadillyTotalTime'] = str((stats_counter['PiccadillyMD'] + stats_counter['PiccadillySD'] +
                                                    stats_counter['PiccadillyPS'] + stats_counter[
                                                        'PiccadillyFS']) * 5) + " seconds."
        stats_counter['VictoriaTotalTime'] = str((stats_counter['VictoriaMD'] + stats_counter['VictoriaSD'] +
                                                  stats_counter['VictoriaPS'] + stats_counter[
                                                      'VictoriaFS']) * 5) + " seconds."
        stats_counter['WaterlooTotalTime'] = str((stats_counter['WaterlooMD'] + stats_counter['WaterlooSD'] +
                                                  stats_counter['WaterlooPS'] + stats_counter[
                                                      'WaterlooFS']) * 5) + " seconds."

    return stats_counter
