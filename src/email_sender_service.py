#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import app_timer
import commands
import data_files
import report_service
import sensor_warnings
import utils

logger = logging.getLogger('app')

send_email_cooldown = datetime.now()
send_report_email_cooldown = datetime.now()


def should_send_email(data):
    global send_email_cooldown
    email_data = data
    if app_timer.is_time_to_send_email(send_email_cooldown):
        email_data['warnings'] = sensor_warnings.get_warnings_as_list(email_data)
        email_data['system'] = commands.get_system_info()
        email_data['log'] = commands.get_lines_from_path('/home/pi/logs/logs.log', 10)
        email_data['healthcheck'] = commands.get_lines_from_path('/home/pi/logs/healthcheck.log', 10)
        send(email_data, 'Measurement')
        send_email_cooldown = datetime.now()


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

        pictures_path = []
        if subject == 'Measurement':
            pictures_path = data['picture_path']

        data = json.dumps(data, indent=2, sort_keys=True)
        message = "Below is a json with a data:\n {}".format(str(data))

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))

        if subject == 'Measurement':
            for picture in pictures_path:
                if picture != "":
                    img_data = open(picture, 'rb').read()
                    image = MIMEImage(img_data, name=os.path.basename(picture))
                    msg.attach(image)

        smtp_server.send_message(msg, cfg['user'], cfg['user'])
        del msg
        smtp_server.quit()
        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email due to {}'.format(e), exc_info=True)
        send_error_log_email("sending email", "Unable to send {} email due to {}.".format(subject, e))


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
        msg['Subject'] = '{} @ {}'.format(subject, utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))
        smtp_server.send_message(msg, cfg['user'], cfg['user'])

        del msg
        smtp_server.quit()

        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email due to {}'.format(e), exc_info=True)


def send_ip_email(device: str):
    cfg = data_files.load_cfg()
    logger.info('Sending email with IP info for device: {}'.format(device))
    try:
        smtp_server = smtplib.SMTP(host=cfg["host"], port=cfg["port"])
        smtp_server.starttls()
        smtp_server.login(cfg['user'], cfg['pass'])

        msg = MIMEMultipart()

        subject = "IP information for {}".format(device)
        message  = "{} starts on  {}".format(device, commands.get_ip())

        msg['From'] = cfg['user']
        msg['To'] = cfg['user']
        msg['Subject'] = '{} @ {}'.format(subject, utils.get_timestamp_title())
        msg.attach(MIMEText(message, 'plain'))
        smtp_server.send_message(msg, cfg['user'], cfg['user'])

        del msg
        smtp_server.quit()

        logger.info('Email sent.')
    except Exception as e:
        logger.error('Unable to send email with IP info for {} due to {}'.format(device,e), exc_info=True)
