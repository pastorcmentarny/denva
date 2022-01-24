#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Author Dominik Symonowicz
* WWW:	https://dominiksymonowicz.com/welcome
* IT BLOG:	https://dominiksymonowicz.blogspot.co.uk
* GitHub:	https://github.com/pastorcmentarny
* Google Play:	https://play.google.com/store/apps/developer?id=Dominik+Symonowicz
* LinkedIn: https://www.linkedin.com/in/dominik-symonowicz
"""

import logging
import os
import shutil

logger = logging.getLogger('app')


def backup_pi_data():
    # copy logs ,reports to
    source = '\\\\DS-LPD-SERVER\\denva\\data\\'
    destination = 'D:\\denva\\backup\\test\\'
    for folderName, subFolders, filenames in os.walk(source):
        print('The current folder is ' + folderName)

        for subFolder in subFolders:
            print('SUBFOLDER OF ' + folderName + ': ' + subFolder)
        for filename in filenames:
            print('FILE INSIDE ' + folderName + ': ' + filename)
            result = shutil.copy(folderName + "\\" + filename, destination)
            print(result)
        print('')


if __name__ == '__main__':
    backup_pi_data()
