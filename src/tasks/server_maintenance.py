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
import os
import shutil
from timeit import default_timer as timer

import config_serivce


def clean_data_bin():
    print('Cleaning data bin')
    data_bin_directory = config_serivce.get_path_for_data_bin()
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
    except OSError as e:  ## if failed, report it back to the user ##
        print("Error: %s - %s." % (e.filename, e.strerror))


def clean():
    start_total_time = timer()
    start_time = timer()
    clean_data_bin()
    print('It took {} ms to delete data bin'.format(int((timer() - start_time) * 1000)))
    print('It took {} ms to complete all tasks.'.format(int((timer() - start_total_time) * 1000)))


if __name__ == '__main__':
    clean()
