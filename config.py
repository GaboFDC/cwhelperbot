#!/usr/bin/env python
# coding=utf-8

import json
import telebot
import logging

# Bot config
info = json.load(open('data/info.json', 'r'))
responses = json.load(open('data/responses.json', 'r'))

bot = telebot.TeleBot(info['token'])
import botmodules

if info['log'] == "1":
    print("Logeo Activado...")
    logger = telebot.logger
    # Outputs debug messages to console.
    telebot.logger.setLevel(logging.DEBUG)
else:
    print("Logeo no activado...")

# Webhook config
WEBHOOK_HOST = info['host']
WEBHOOK_PORT = info['port']
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = info['ssl_cert']
WEBHOOK_SSL_PRIV = info['ssl_priv']  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (info['token'])
