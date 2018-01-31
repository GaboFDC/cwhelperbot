#!/usr/bin/env python
# coding=utf-8

from config import *


# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    if info['admin_cid']:
        bot.reply_to(message, message.text)
    else:
        bot.reply_to(message, responses['not_admin'] % m.from_user.first_name)

