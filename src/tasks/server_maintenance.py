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
import datetime
import os
import shutil
from timeit import default_timer as timer

import config_service


def clean_data_bin():
    print('Cleaning data bin')
    data_bin_directory = config_service.get_path_for_data_bin()
    if not os.path.isdir(data_bin_directory):
        print('data bin directory do not exists. Recreating.')
        os.mkdir(data_bin_directory)
        print('clean data bin not needed.')
        return

    try:
        print('removing unused data')
        shutil.rmtree(data_bin_directory)
        print('recreate a directory')
        os.mkdir(data_bin_directory)
        print('clean data bin complete.')
    except OSError as exception:
        print("Error: %s - %s." % (exception.filename, exception.strerror))


def clean():
    start_total_time = timer()
    start_time = timer()
    clean_data_bin()
    print('It took {} ms to delete data bin'.format(int((timer() - start_time) * 1000)))
    print('It took {} ms to complete all tasks.'.format(int((timer() - start_total_time) * 1000)))


def reminders():
    if datetime.datetime.now().year >= 2021:
        print("PLEASE UPDATE  EVENTS AND CELEBRATIONS!"
              " UPDATE DATE THAT VARY EVERY YEAR! "
              "After that update this method to next year :)")


def backup_pictures_from_previous_day():
    # if folder exists , finish
    # create a folder
    # count files in folder
    # copy pictures
    # log result
    pass


if __name__ == '__main__':
    clean()
    reminders()
