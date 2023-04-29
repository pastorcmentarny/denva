# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import datetime
import logging

import dom_utils

logger = logging.getLogger("app")

events = {
    "0101": ["New year day"],
    "0110": ["World's first Underground railway opened"],
    "0121": ["Dzien Babci"],
    "0122": ["Dzien Dziadka"],
    "0123": ["Java was released in 1996"],
    "0125": ["St Dwynwen's Day, Welsh patron saint of lovers"],
    "0209": ["Boeing 747 makes its first flight"],
    "0227": ["Leonard Nimoy died in 2015"],
    "0301": ["St David’s Day, patron of Wales."],
    "0302": ["Concorde makes its first flight"],
    "0308": ["International Women Day"],
    "0312": ["Terry Pratchett passed away"],
    "0317": ["St Patrick's Day, patron to of Northern Ireland."],
    "0320": ["Spring starts"],
    "0326": ["Leonard Nimoy was born 1931"],
    "0401": ["Prima Aprilis"],
    "0422": ["International Earth Day"],
    "0423": ["St George's Day"],
    "0426": ["The Chernobyl disaster 1986"],
    "0428": ["Terry Prattchet was born in 1948"],
    "0501": ["Labour Day"],
    "0502": ["Dzień Flagi Rzeczpospolitej Polskiej"],
    "0503": ["Święto Konstytucji 3 Maja"],
    "0509": ["European Union Day"],
    "0523": ["Java language anniversary"],
    "0526": ["Mother day"],
    "0601": ["Children day"],
    "0605": ["Wybory(1989) które zmieniły Polskę"],
    "0609": ["George Stephenson born (build world's first locomotive)"],
    "0620": ["Summer starts", "Longest day in the year"],
    "0621": ["Father day[UK]"],
    "0623": ["Dzień Ojca [PL]"],
    "0720": ["Nei Armstrong takes his 1st step on Moon"],
    "0723": ["The original Commodore Amiga is released"],
    "0819": ["Gene roddenberry was born"],
    "0922": ["Autumn starts"],
    "0930": ["Dzień Chłopaka"],
    "1004": ["Sputnik 1 launch (first artificial satellite)"],
    "1101": ["Wszystkich Świętych"],
    "1102": ["Dzień zaduszny"],
    "1107": ["Hug a Bear Day"],
    "1114": ["BBC makes its first radio broadcast"],
    "1031": ["St. Andrew Day ,Andrzejki?"],
    "1111": ["Narodowe święto Niepodległości"],
    "1129": ["Andrzejki"],
    "1204": ["Barborka (Dzień Górnika)"],
    "1206": ["Dzień św. Mikołaja"],
    "1221": ["Winter starts", "Shortest day of the year"],
    "1224": ["Christmas Eve","The crew of Apollo 8 was first human to orbit the moon"],
    "1225": ["Christmas day"],
    "1226": ["Boxing day"],
    "1231": ["New year Eve"],
}

"""
DO NOT FORGOT TO UPDATE BY END OF 2023
To have 2 events on one day do this : ["Easter", "Święto Qingming"],
"""


movable_events = {
    "0122": ["Chinese new year"],  # 2023
    "0326": ["Summertime +1hr :("],  # 2023
    "0405": ["Easter Monday", "Święto Qingming"],  # 2023
    "0407": ["Good Friday"],  # 2023
    "0409": ["Easter"],  # 2023
    "0501": ["Early May Bank Holiday"],  # 2023
    "0514": ["Mother's day (China)"],  # 2023
    "0529": ["Late May Bank Holiday"],  # 2023
    "0622": ["端午节(Dragon Boat Festival)"],  # 2023
    "0623": ["端午节(Dragon Boat Festival)"],  # 2023
    "0624": ["端午节(Dragon Boat Festival)"],  # 2023
    "0828": ["Late Summer Bank Holiday"],
    "0929": ["Mid-Autumn Festival"],
    "1030": ["Wintertime -1hr :)"],
}

all_events = dom_utils.merge_two_dictionaries(events, movable_events)


def get_today() -> list:
    return all_events.get(dom_utils.get_timestamp_key(), [])


def day_left_text(counter: int) -> str:
    if counter == 0:
        return "today"
    elif counter == 1:
        return "tomorrow"
    elif counter > 1:
        return "{} days left".format(counter)
    else:
        logger.warning("Unsupported day left counter {}".format(counter))
        return "error"


def get_sentence_from_list_of_events(event_list: list) -> str:
    if len(event_list) == 1:
        return event_list[0]
    elif len(event_list) == 2:
        return "{} and {}".format(event_list[0], event_list[1])
    elif len(event_list) > 2:
        sentence = ""
        for an_event in event_list[0:len(event_list) - 1]:
            sentence = sentence + an_event + " "
        return "{}and {}".format(sentence, event_list[len(event_list) - 1])


def get_next_3_events() -> list:
    next3events = []
    day = datetime.datetime.now()
    counter = 0
    while len(next3events) < 3:
        event = all_events.get(dom_utils.get_timestamp_key(day))
        if event is not None:
            next3events.append("{} ({})".format(get_sentence_from_list_of_events(event), day_left_text(counter)))
        day = day + datetime.timedelta(days=1)
        counter = counter + 1
    return next3events
