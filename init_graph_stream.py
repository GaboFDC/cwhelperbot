#!/usr/bin/env python
# coding=utf-8

import os
import sys
import plotly.plotly as py
import plotly.tools as tls
from dotenv import load_dotenv
from plotly.graph_objs import *
from os.path import join, dirname

if sys.argv[1] == "deals":
    offset = 0
elif sys.argv[1] == "offers":
    offset = 18
else:
    print("Wrong argument")
    exit()

print("Running with {} offset".format(offset))
user_allow = input("Continue?")


if user_allow != "Y":
    exit()

# ENV
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Ploty conf
tls.set_credentials_file(
    username=os.environ['PLOTLY_USER'], api_key=os.environ['PLOTLY_PASS'])
tls.set_config_file(world_readable=True, sharing='public')
tls.set_credentials_file(stream_ids=os.environ['PLOTLY_STREAM_IDS'].split(','))
stream_ids = tls.get_credentials_file()['stream_ids']

scatter_list = []
items_list = []

with open('items.txt') as f:
    for line in f:
        items_list.extend(line.split(','))
for i, item in enumerate(items_list):
    print("item {} - index {}".format(item, i + offset))
    scatter_list.append(
        Scatter(
            y=[],
            x=[],
            name='{} {} price'.format(item, sys.argv[1]),
            mode='lines+markers',
            stream=Stream(token=stream_ids[i + offset], maxpoints=10000)
        )
    )

data = Data(scatter_list)

layout = dict(
    title="Chat Wars {}".format(sys.argv[1]),
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='minute',
                     stepmode='backward'),
                dict(count=10,
                     label='10m',
                     step='minute',
                     stepmode='backward'),
                dict(count=1,
                     label='1h',
                     step='hour',
                     stepmode='backward'),
                dict(count=6,
                     label='6h',
                     step='hour',
                     stepmode='backward'),
                dict(count=1,
                     label='1d',
                     step='day',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
)

fig = Figure(data=data, layout=layout)
unique_url = py.plot(fig, filename='chat-wars-{}-stream'.format(sys.argv[1]))
