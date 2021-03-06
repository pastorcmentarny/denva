# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* Github:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import datetime
import logging

from common import dom_utils

logger = logging.getLogger('app')

events = {
    '0101': ['New year day'],
    '0121': ["Dzien Babci"],
    '0122': ["Dzien Dziadka"],
    '0123': ["Java was released in 1996"],
    '0308': ["International Women Day"],
    '0312': ['Terry Pratchett passed away'],
    '0320': ['Spring starts'],
    '0401': ['Prima Aprilis'],
    '0422': ['International Earth Day'],
    '0428': ['Terry Prattchet was born in 1948'],
    '0501': ['Labour Day'],
    '0502': ['Dzień Flagi Rzeczpospolitej Polskiej'],
    '0503': ['Święto Konstytucji 3 Maja'],
    '0509': ['European Union Day'],
    '0523': ['Java language anniversary'],
    '0526': ['Mother day'],
    '0601': ['Children day'],
    '0620': ['Summer starts', 'Longest day in the year'],
    '0621': ['Father day[UK]'],
    '0623': ['Dzień Ojca [PL]'],
    '0922': ['Autumn starts'],
    '0930': ['Dzień Chłopaka'],
    '1101': ['Wszystkich Świętych'],
    '1102': ['Dzień zaduszny'],
    '1107': ['Hug a Bear Day'],
    '1111': ['Narodowe święto Niepodległości'],
    '1129': ['Andrzejki'],
    '1204': ['Barborka (Dzień Górnika)'],
    '1206': ['Dzień św. Mikołaja'],
    '1221': ['Winter starts', 'Shortest day of the year'],
    '1224': ['Christmas Eve'],
    '1225': ['Christmas day'],
    '1226': ['Boxing day'],
    '1231': ['New year Eve'],
}

# DO NOT FORGOT TO UPDATE BY END OF 2021
movable_events = {
    '0212': ["Chinese new year"],
    '0328': ['Sumertime +1hr :('],
    '0402': ['Good Friday'],
    '0404': ['Easter'],
    '0405': ['Easter Monday'],
    '0503': ['Early May Bank Holiday'],
    '0531': ['Late May Bank Holiday'],
    '0830': ['Late Summer Bank Holiday'],
    '1031': ['Wintertime -1hr :)'],
}

all_events = dom_utils.merge_two_dictionaries(events, movable_events)


def get_today() -> list:
    return all_events.get(dom_utils.get_timestamp_key(), [])


def day_left_text(counter: int) -> str:
    if counter == 0:
        return 'today'
    elif counter == 1:
        return 'tomorrow'
    elif counter > 1:
        return '{} days left'.format(counter)
    logger.warning('Unsupported day left counter {}'.format(counter))


def get_sentence_from_list_of_events(event_list: list) -> str:
    if len(event_list) == 1:
        return event_list[0]
    elif len(event_list) == 2:
        return '{} and {}'.format(event_list[0], event_list[1])
    elif len(event_list) > 2:
        sentence = ''
        for an_event in event_list[0:len(event_list) - 1]:
            sentence = sentence + an_event + " "
        return '{}and {}'.format(sentence, event_list[len(event_list) - 1])


def get_next_3_events() -> list:
    next3events = []
    day = datetime.datetime.now()
    counter = 0
    while len(next3events) < 3:
        event = all_events.get(dom_utils.get_timestamp_key(day))
        if event is not None:
            next3events.append('{} ({})'.format(get_sentence_from_list_of_events(event), day_left_text(counter)))
        day = day + datetime.timedelta(days=1)
        counter = counter + 1
    return next3events
