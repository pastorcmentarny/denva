# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""


class Status:
    OK = 2
    WARN = 1
    ERROR = 0

    state = OK

    def __init__(self, state: int = 2):
        self.state = state

    def set_warn(self):
        if self.state == 2:
            self.state = 1

    def set_error(self):
        self.state = 0

    def get_status_as_light_colour(self):
        if self.state == 2:
            return 'GREEN'
        elif self.state == 1:
            return 'ORANGE'
        elif self.state == 0:
            return 'RED'
        else:
            print('UNKNOWN STATE {}'.format(self.state))
            return 'UNKNOWN'
