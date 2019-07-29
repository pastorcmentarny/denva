#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def get_warnings_for(year: str, month: str, day: str) -> list:
    return get_warnings('/home/pi/logs/warnings.log.{}-0{}-{}'.format(str(year), str(month), str(day)))  # fix 0x


def get_warnings_for_today() -> list:
    return get_warnings('/home/pi/logs/warnings.log')


def get_warnings(path: str) -> list:
    file = open(path, 'r', newline='')
    content = file.readlines()
    content.insert(0, 'Warning counts: {}'.format(len(content)))
    return content
