#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import utils


def print_measurement(data, left_width, right_width):
    print_title(left_width, right_width)
    print_items(data, left_width, right_width)
    print('-' * 36 + '\n')


def print_items(data, left_width, right_width):
    for title, value in data.items():
        print(title.ljust(left_width, '.') + str(value).rjust(right_width, ' '))


def print_title(left_width, right_width):
    title = 'Measurement @ {}'.format(utils.get_timestamp_title())
    print(title.center(left_width + right_width, "-"))
