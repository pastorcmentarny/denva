#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
import datetime
import logging

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger('app')


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
