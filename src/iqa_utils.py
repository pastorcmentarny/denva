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

result = {
    'score': 'unknown',
    'value': 0,
    'action': 'unknown',
    'information': 'unknown'
}


# based on https://www.idt.com/eu/en/document/whp/overview-tvoc-and-indoor-air-quality
def get_iqa_for_tvoc(tvoc: str) -> dict:
    tvoc_value = int(tvoc)
    if tvoc_value < 150:
        result['score'] = 'Very Good'
        result['value'] = tvoc_value
        result['action'] = 'No action required'
        result['information'] = 'Clean air'
    elif tvoc_value < 500:
        result['score'] = 'Good'
        result['value'] = tvoc_value
        result['action'] = 'Ventilation recommended.'
        result['information'] = 'Good Air Quality'
    elif tvoc_value < 1500:
        result['score'] = 'Medium'
        result['value'] = tvoc_value
        result['action'] = 'Ventilation required.'
        result['information'] = 'Air Quality is not good. (Not recommended for exposure for than year)'
    elif tvoc_value < 5000:
        result['score'] = 'POOR'
        result['value'] = tvoc_value
        result['action'] = 'Ventilate now!'
        result['information'] = 'Air Quality is POOR. (Not recommended for exposure for than month)'
    else:
        result['score'] = 'BAD'
        result['value'] = tvoc_value
        result['action'] = 'Use only if unavoidable!'
        result['information'] = 'Unacceptable Air Quality! Use only if unavoidable and only for short periods.'

    return result
