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
    OK = 3
    CAUTION = 2
    WARN = 1
    ERROR = 0

    state = OK

    def __init__(self, state: int = 3):
        self.state = state

    def set_warn(self):
        if self.state == 3:
            self.state = 2

    def set_danger(self):
        self.state = 1

    def set_error(self):
        self.state = 0

    def get_status_as_light_colour(self):
        if self.state == 3:
            return 'OK'
        elif self.state == 2:
            return 'CAUTION'
        elif self.state == 1:
            return 'WARN'
        elif self.state == 0:
            return 'ERROR'
        else:
            print('UNKNOWN STATE {}'.format(self.state))
            return 'UNKNOWN'
