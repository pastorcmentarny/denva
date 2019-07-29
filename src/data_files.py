#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path


def load_cfg() -> dict:
    path = '/home/pi/email.json'
    with open(path, 'r') as email_config:
        return json.load(email_config)


def save_report(report: dict, file: str):
    with open('/home/pi/reports/{}'.format(file), 'w+', encoding='utf-8') as report_file:
        json.dump(report, report_file, ensure_ascii=False, indent=4)


def load_report(report_date: str) -> dict:
    path = '/home/pi/reports/{}'.format(report_date)
    with open(path, 'r') as report_file:
        return json.load(report_file)


def check_if_report_was_generated(report_date: str) -> bool:
    path = '/home/pi/reports/{}'.format(report_date)
    return os.path.isfile(path)
