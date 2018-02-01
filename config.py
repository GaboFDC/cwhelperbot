#!/usr/bin/env python
# coding=utf-8

import os
import json
import telebot
import logging

# Bot config
bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
import botmodules

if os.environ['LOG_ENABLED'] == "1":
    print("Logeo Activado...")
    logger = telebot.logger
    # Outputs debug messages to console.
    telebot.logger.setLevel(logging.DEBUG)
else:
    print("Logeo no activado...")

# Webhook config
WEBHOOK_HOST = os.environ['WEBHOOK_HOST']
WEBHOOK_PORT = int(os.environ['WEBHOOK_PORT'])
APP_PORT = int(os.environ['PORT'])
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (os.environ['BOT_TOKEN'])