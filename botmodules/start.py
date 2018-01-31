#!/usr/bin/env python
# coding=utf-8

from config import *


@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    uid = m.from_user.id
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, responses['start'] % m.from_user.first_name)
