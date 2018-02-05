#!/usr/bin/env python
# coding=utf-8

import os
import pika
import json
import atexit
import datetime
from config import *
import plotly.plotly as py
import plotly.tools as tls
from dotenv import load_dotenv
from pymongo import MongoClient
from os.path import join, dirname

# ENV
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# DB
if os.environ['USE_DB'] == 1:
    print("Using mongo db")
    client = MongoClient('localhost', 32769)
    db = client['cwhelper']
    offers_collection = db.offers
    offers_collection = db.offers

# Ploty conf
tls.set_credentials_file(
    username=os.environ['PLOTLY_USER'], api_key=os.environ['PLOTLY_PASS'])
tls.set_config_file(world_readable=True, sharing='public')
tls.set_credentials_file(stream_ids=os.environ['PLOTLY_STREAM_IDS'].split(','))
stream_ids = tls.get_credentials_file()['stream_ids']
s0 = py.Stream(stream_ids[18])
s1 = py.Stream(stream_ids[19])
s2 = py.Stream(stream_ids[20])
s3 = py.Stream(stream_ids[21])
s4 = py.Stream(stream_ids[22])
s5 = py.Stream(stream_ids[23])
s6 = py.Stream(stream_ids[24])
s7 = py.Stream(stream_ids[25])
s8 = py.Stream(stream_ids[26])
s9 = py.Stream(stream_ids[27])
s10 = py.Stream(stream_ids[28])
s11 = py.Stream(stream_ids[29])
s12 = py.Stream(stream_ids[30])
s13 = py.Stream(stream_ids[31])
s14 = py.Stream(stream_ids[32])
s15 = py.Stream(stream_ids[33])
s16 = py.Stream(stream_ids[34])
s17 = py.Stream(stream_ids[35])
s0.open()
s1.open()
s2.open()
s3.open()
s4.open()
s5.open()
s6.open()
s7.open()
s8.open()
s9.open()
s10.open()
s11.open()
s12.open()
s13.open()
s14.open()
s15.open()
s16.open()
s17.open()


# Chat Wars API (RabbitMQ)
parameters = pika.URLParameters(
    'amqps://{}:{}@api.chatwars.me:5673/'.format(
        os.environ['CWAPI_USER'], os.environ['CWAPI_PASS']))
parameters.socket_timeout = 5
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


def offer_send_to_stream(body):
    offer = json.loads(body)
    if offer['price'] < 500:
        offer['timestamp'] = datetime.datetime.now().timestamp()
        if os.environ['USE_DB'] == 1:
            offers_collection.insert_one(offer)
        if offer['item'] == 'Steel':
            s10.write(dict(x=datetime.datetime.now(), y=offer['price']))
            if offer['price'] < 11:
                bot.send_message(os.environ['TG_ADMIN_UID'], "OFFER!\n{} - price: {}".format(offer['item'], offer['price']))
        elif offer['item'] == 'Thread':
            s0.write(dict(x=datetime.datetime.now(), y=offer['price']))
            if offer['price'] < 9:
                bot.send_message(os.environ['TG_ADMIN_UID'], "OFFER!\n{} - price: {}".format(offer['item'], offer['price']))
        elif offer['item'] == 'Stick':
            s1.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Pelt':
            s2.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Bone':
            s3.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Coal':
            s4.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Charcoal':
            s5.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Powder':
            s6.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Iron ore':
            s7.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Cloth':
            s8.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Magic Stone':
            s9.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Leather':
            s11.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Bone powder':
            s12.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'String':
            s13.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Coke':
            s14.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Pouch of gold':
            s15.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Torch':
            s16.write(dict(x=datetime.datetime.now(), y=offer['price']))
        elif offer['item'] == 'Wrapping':
            s17.write(dict(x=datetime.datetime.now(), y=offer['price']))
        else:
            print("\033[91m Couldn't find item type {} \033[0m".format(offer))


def process_offers(ch, method, properties, body):
    print(" [x] Received OFFER %r" % body)
    offer_send_to_stream(body)


channel.basic_consume(process_offers,
                      queue="{}_offers".format(os.environ['CWAPI_USER']),
                      no_ack=True)


def close_all():
    print("\033[91m  CLEAN UP \033[0m")
    connection.close()
    s1.close()
    s2.close()
    s3.close()
    s4.close()
    s5.close()
    s6.close()
    s7.close()
    s8.close()
    s9.close()
    s10.close()
    s11.close()
    s12.close()
    s13.close()
    s14.close()
    s15.close()


atexit.register(close_all)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
