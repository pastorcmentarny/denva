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
from datetime import datetime
import logging
import os
import re
import subprocess
import time
import utils

import email_sender_service

logger = logging.getLogger('app')

step = 0.1
photo_dir = ''


def mouth_all_drives():
    logger.info('mounting external partion for pictures')
    try:
        cmd = 'sudo mount -t auto -v /dev/mmcblk0p3 /mnt/data'
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.info(str(ps.communicate()[0]))
        cmd = 'sudo mount -a'
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.info(str(ps.communicate()[0]))
    except Exception as e:
        error_message = "Unable to mount drive due to {}".format(e)
        email_sender_service.send_error_log_email("mount drive", error_message)
        logger.warning('Something went badly wrong..', exc_info=True)


def capture_picture() -> str:
    try:
        date_path = datetime.now().strftime("%Y/%m/%d")
        path = "/mnt/data/photos/{}/".format(date_path)
        if not os.path.isdir(path):
            logger.info('creating folder for ()'.format(path))
            os.makedirs(path)
        date = utils.get_timestamp_file()
        photo_path = "/mnt/data/photos/{}/{}.jpg".format(date_path, date)
        cmd = "fswebcam -r 1280x960 --no-banner {}".format(photo_path)
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        total_time = step
        while not os.path.exists(photo_path):
            time.sleep(step)
            total_time += step
        time.sleep(2)
        logger.info('it took {:.2f} seconds to capture picture'.format(total_time))
        return photo_path
    except Exception as e:
        logger.warning('Something went badly wrong\n{}'.format(e), exc_info=True)
        email_sender_service.send_error_log_email("camera", "Unable to capture picture due to {}".format(e))
    return ""


def get_cpu_speed():
    cmd = "find /sys/devices/system/cpu/cpu[0-3]/cpufreq/scaling_cur_freq -type f | xargs cat | sort | uniq -c"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.communicate()[0]
    output = str(output)
    output = output.strip()[4:len(output) - 3].strip()[2:]  # i am sorry ..
    try:
        output = str(float(output) / 1000)
    except ValueError:
        logger.warning(output)
        return 'CPU: variable speed'
    return output + ' Mhz'


def get_cpu_temp():
    return str(subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_temp']), "utf-8") \
        .strip().replace('temp=', '')


def get_ip() -> str:
    text = str(subprocess.check_output(['ifconfig', 'wlan0']), "utf-8")
    start, end = text.find('inet'), text.find('netmask')
    result = text[start + 4: end]
    return result.strip()


def get_uptime() -> str:
    return str(subprocess.check_output(['uptime', '-p']), "utf-8") \
        .strip() \
        .replace('weeks', 'w').replace('week', 'w') \
        .replace('days', 'd').replace('day', 'd') \
        .replace('hours', 'h').replace('hour', 'h') \
        .replace('minutes', 'm').replace('minute', 'm')


def get_system_info() -> dict:
    return {
        'CPU Speed': get_cpu_speed(),
        'CPU Temp': get_cpu_temp(),
        'IP': get_ip(),
        'Uptime': get_uptime(),
        'Free Space:': get_space_available() + 'MB',
        'Data Free Space:': get_data_space_available() + 'MB'
    }


def get_space_available():
    p = subprocess.Popen("df / -m --output=avail", stdout=subprocess.PIPE, shell=True)
    result, _ = p.communicate()
    return re.sub('[^0-9.]', '', str(result).strip())


def get_data_space_available():
    p = subprocess.Popen("df /mnt/data -m --output=avail", stdout=subprocess.PIPE, shell=True)
    result, _ = p.communicate()
    return re.sub('[^0-9.]', '', str(result).strip())


def get_lines_from_path(path: str, lines: int) -> dict:
    text = str(subprocess.check_output(['tail', '-n', str(lines), path]).strip(), "utf-8").split('\n')
    return utils.convert_list_to_dict(text)


def get_last_line_from_log(path: str) -> str:
    text = str(subprocess.check_output(['tail', '-n', "1", path]).strip(), "utf-8")
    return text


def get_last_photo_filename() -> str:
    current_time = datetime.now()
    cmd = f"ls /mnt/data/photos/{current_time.year}/{current_time.month:02d}/{current_time.day:02d}/ -rt | tail -1"
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ps.communicate()[0]
    return str(result, 'utf-8')


def reboot(reason: str):
    logger.warning("Rebooting device due to: {}".format(reason))
    subprocess.check_output(['sudo', 'reboot'])
