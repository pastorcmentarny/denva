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
import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from common import app_timer
from common import commands, data_files, dom_utils
from reports import report_service
from services import sensor_warnings_service

logger = logging.getLogger('app')

send_denva_email_cooldown = datetime.now()
send_report_email_cooldown = datetime.now()


def should_send_email(data):
    global send_denva_email_cooldown
    email_data = data
    if app_timer.is_time_to_send_email(send_denva_email_cooldown):
        logger.info('Collecting data')
        email_data['warnings'] = sensor_warnings_service.get_warnings_as_list(email_data)
        email_data['system'] = commands.get_system_info()
        email_data['log'] = commands.get_lines_from_path('/home/pi/logs/logs.log', 10)
        email_data['healthcheck'] = commands.get_lines_from_path('/home/pi/logs/healthcheck.log', 10)
        send(email_data, 'Measurement')
        send_denva_email_cooldown = datetime.now()


def should_send_email_v2(data):
    send(data, 'Data')


def should_send_report_email():
    global send_report_email_cooldown
    if app_timer.is_time_to_send_report_email(send_report_email_cooldown):
        result = report_service.generate_for_yesterday()
        if not result:
            send_report_email_cooldown = datetime.now()
            logger.info("Daily report email sent.")


def send(data: dict, subject: str):
    cfg = data_files.load_cfg()
    logger.info('Sending email for {}'.format(subject))
    try:
        smtp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        smtp_server.starttls()
        smtp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()

        data = json.dumps(data, indent=2, sort_keys=True)
        message = "Below is a json with a data:\n {}".format(str(data))

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, dom_utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))

        smtp_server.send_message(msg, cfg['user'], cfg['user'])
        del msg
        smtp_server.quit()
        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email due to {}'.format(e), exc_info=True)


def send_picture(picture_path: str, pict_no: int):
    cfg = data_files.load_cfg()
    subject = "CCTV"
    logger.info('Sending email for {}'.format(subject))
    try:
        smtp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        smtp_server.starttls()
        smtp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()

        message = "This is picture from PI Camera no. {} from path".format(pict_no, picture_path)

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, dom_utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))

        img_data = open(picture_path, 'rb').read()
        image = MIMEImage(img_data, name=os.path.basename(picture_path))
        msg.attach(image)

        smtp_server.send_message(msg, cfg['user'], cfg['user'])
        del msg
        smtp_server.quit()
        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email due to {}'.format(e), exc_info=True)


def send_error_log_email(what: str, message: str):
    cfg = data_files.load_cfg()
    logger.info('Sending error log email with message: {}'.format(message))
    try:
        smtp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        smtp_server.starttls()
        smtp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()

        subject = "An serious error happen while {}".format(what)
        message = "Whoops.. Some sort of gobshite happen with app.\n Error message is: {}".format(message)

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, dom_utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))
        smtp_server.send_message(msg, cfg['user'], cfg['user'])

        del msg
        smtp_server.quit()

        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email due to {}'.format(e), exc_info=True)


def send_ip_email(device: str):
    logger.info('Sending email with IP info for device: {}'.format(device))
    cfg = data_files.load_cfg()
    try:
        smtp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        smtp_server.starttls()
        smtp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()

        subject = "IP information for {}".format(device)
        message = "{} starts on  {}".format(device, commands.get_ip())

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, dom_utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))
        smtp_server.send_message(msg, cfg['user'], cfg['user'])

        del msg
        smtp_server.quit()
        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email with IP info for {} due to {}'.format(device, e), exc_info=True)
