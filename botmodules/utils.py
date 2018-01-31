#!/usr/bin/env python
# coding=utf-8

from config import *


@bot.message_handler(commands=['util'])
def send_util(m):
    cid = m.chat.id
    uid = m.from_user.id
    bot.send_message(cid, "cid: "+str(cid)+" uid; "+str(uid))
