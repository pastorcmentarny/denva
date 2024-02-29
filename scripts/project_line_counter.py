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

import os.path
import pathlib
from datetime import datetime

from itertools import chain

line_count = 0
file_count = 0
result_file = str(pathlib.PurePath("D:/GitHub/denva/scripts/","project_line_counter.py"))

paths = ("D:\\GitHub\\denva\\src\\", "D:\\GitHub\\denva\\scripts\\")
for path, _, files in chain.from_iterable(os.walk(path) for path in paths):
    for name in files:
        file_path = pathlib.PurePath(path, name)
        if str(file_path).endswith(".py") or str(file_path).endswith(".sh"):
            with open(str(file_path), encoding=config.ENCODING) as f:
                file_count += 1
                for line in f:
                    line_count += 1

result = (f"# {datetime.now()}.There are {file_count} files in the project and total count of lines is: {line_count}")
with open(result_file, config.APPEND_WITH_READ_MODE, newline='') as local_file:
    local_file.write(result)
    local_file.write('\n')

# Results
# 2020-06-07 19:52:09.065886.There are 89 files in the project and total count of lines is: 8694

