#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import datetime
import logging
from datetime import timedelta

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import app_timer
import data_files
import commands
import utils
import sensor_warnings

logger = logging.getLogger('app')

send_email_cooldown = datetime.datetime.now()


def should_send_email(data):
    global send_email_cooldown
    email_data = data
    if app_timer.is_time_to_send_email(send_email_cooldown):
        email_data['warnings'] = sensor_warnings.get_warnings_as_list(email_data)
        email_data['system'] = commands.get_system_info()
        send(email_data, data_files.load_cfg())
        send_email_cooldown = datetime.datetime.now()


def send_report(data: dict, cfg: dict):
    try:
        stmp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        stmp_server.starttls()
        stmp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()  # create a message

        message = "Below is a json with a data:\n {}".format(str(data))
        today = datetime.datetime.now()
        yesterday = today - timedelta(days=1)

        msg['From'] = cfg['user']  # from me
        msg['To'] = cfg['user']  # to me
        msg['Subject'] = 'Report @ {}'.format(yesterday.strftime("%Y-%m-%d %H:%M:%S"))
        msg.attach(MIMEText(message, 'plain'))

        stmp_server.send_message(msg, cfg['user'], cfg['user'])
        del msg
        stmp_server.quit()
    except Exception:
        logger.warning("Unable to send email")


# TODO add verify data and cfg
def send(data: dict, cfg: dict):

    try:
        stmp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        stmp_server.starttls()
        stmp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()       # create a message

        message = "Below is a json with a data:\n {}".format(str(data))

        msg['From']=cfg['user'] # from me
        msg['To']=cfg['user']  # to me
        msg['Subject'] = 'Measurement @ {}'.format(utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))

        stmp_server.send_message(msg,cfg['user'],cfg['user'])
        del msg
        stmp_server.quit()
    except Exception:
        logger.warning("Unable to send email")
