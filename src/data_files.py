#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def load_cfg() -> dict:
    path = '/home/pi/email.json'
    with open(path, 'r') as email_config:
        return json.load(email_config)
