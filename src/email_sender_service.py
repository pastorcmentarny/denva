#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import datetime
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import app_timer
import data_files
import warning_utils

logger = logging.getLogger('app')


def should_send_email(data, send_email_cooldown):
    email_data = data
    if app_timer.is_time_to_send_email(send_email_cooldown):
        email_data['warnings'] = warning_utils.get_warnings_as_list(email_data)
        send(email_data, data_files.load_cfg())
        return datetime.datetime.now()
    else:
        return send_email_cooldown


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
        msg['Subject']=  'Measurement @ {}'.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        msg.attach(MIMEText(message, 'plain'))

        stmp_server.send_message(msg,cfg['user'],cfg['user'])
        del msg
        stmp_server.quit()
    except Exception:
        logger.warning("Unable to send email")
