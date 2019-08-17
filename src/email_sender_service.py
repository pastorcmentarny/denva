#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from datetime import datetime
import logging
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import app_timer
import data_files
import commands
import report_service
import utils
import sensor_warnings

logger = logging.getLogger('app')

send_email_cooldown = datetime.now()
send_report_email_cooldown = datetime.now()


def should_send_email(data):
    global send_email_cooldown
    email_data = data
    if app_timer.is_time_to_send_email(send_email_cooldown):
        email_data['warnings'] = sensor_warnings.get_warnings_as_list(email_data)
        email_data['system'] = commands.get_system_info()
        send(email_data, data_files.load_cfg(), 'Measurement')
        send_email_cooldown = datetime.now()


def should_send_report_email():
    global send_report_email_cooldown
    if app_timer.is_time_to_send_report_email(send_report_email_cooldown):
        result = report_service.generate_for_yesterday()
        if not result:
            send_report_email_cooldown = datetime.now()
        logger.warning("Unable to send email with report")


def send(data: dict, cfg: dict, subject: str):
    try:
        smtp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        smtp_server.starttls()
        smtp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()
        data = json.dumps(data, indent=2, sort_keys=True)
        message = "Below is a json with a data:\n {}".format(str(data))

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))

        smtp_server.send_message(msg, cfg['user'], cfg['user'])
        del msg
        smtp_server.quit()
    except Exception:
        logger.warning("Unable to send email")
