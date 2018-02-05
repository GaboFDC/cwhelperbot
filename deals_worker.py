#!/usr/bin/env python
# coding=utf-8

import os
import pika
import json
import atexit
import datetime
import plotly.plotly as py
import plotly.tools as tls
from dotenv import load_dotenv
from pymongo import MongoClient
from os.path import join, dirname

# DB
client = MongoClient('localhost', 32769)
db = client['cwhelper']
deals_collection = db.deals
offers_collection = db.offers

# ENV
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Ploty conf
tls.set_credentials_file(
    username=os.environ['PLOTLY_USER'], api_key=os.environ['PLOTLY_PASS'])
tls.set_config_file(world_readable=True, sharing='public')
stream_ids = tls.get_credentials_file()['stream_ids']
s0 = py.Stream(stream_ids[0])
s1 = py.Stream(stream_ids[1])
s2 = py.Stream(stream_ids[2])
s3 = py.Stream(stream_ids[3])
s4 = py.Stream(stream_ids[4])
s5 = py.Stream(stream_ids[5])
s6 = py.Stream(stream_ids[6])
s7 = py.Stream(stream_ids[7])
s8 = py.Stream(stream_ids[8])
s9 = py.Stream(stream_ids[9])
s10 = py.Stream(stream_ids[10])
s11 = py.Stream(stream_ids[11])
s12 = py.Stream(stream_ids[12])
s13 = py.Stream(stream_ids[13])
s14 = py.Stream(stream_ids[14])
s15 = py.Stream(stream_ids[15])
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

# Chat Wars API (RabbitMQ)
parameters = pika.URLParameters(
    'amqps://{}:{}@api.chatwars.me:5673/'.format(
        os.environ['CWAPI_USER'], os.environ['CWAPI_PASS']))
parameters.socket_timeout = 5
connection = pika.BlockingConnection(parameters)
channel = connection.channel()


def deal_send_to_stream(body):
    deal = json.loads(body)
    deal['timestamp'] = datetime.datetime.now().timestamp()
    deals_collection.insert_one(deal)
    if deal['item'] == 'Thread':
        s0.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Stick':
        s1.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Pelt':
        s2.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Bone':
        s3.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Coal':
        s4.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Charcoal':
        s5.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Powder':
        s6.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Iron ore':
        s7.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Cloth':
        s8.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Magic Stone':
        s9.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Steel':
        s10.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Leather':
        s11.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Bone powder':
        s12.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'String':
        s13.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Coke':
        s14.write(dict(x=datetime.datetime.now(), y=deal['price']))
    elif deal['item'] == 'Pouch':
        s15.write(dict(x=datetime.datetime.now(), y=deal['price']))
    else:
        print("\033[91m Couldn't find item type {} \033[0m".format(deal))


def process_deals(ch, method, properties, body):
    print(" [x] Received DEAL %r" % body)
    deal_send_to_stream(body)


channel.basic_consume(process_deals,
                      queue="{}_deals".format(os.environ['CWAPI_USER']),
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
