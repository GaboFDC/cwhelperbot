#!/usr/bin/env python
# coding=utf-8

import os
import plotly
import datetime
import plotly.plotly as py
from dotenv import load_dotenv
from pymongo import MongoClient
from os.path import join, dirname
from plotly.graph_objs import Layout, Scatter

# ENV
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# DB
client = MongoClient('localhost', 32769)
db = client['cwhelper']
collection = db.deals

# Ploty conf
plotly.tools.set_credentials_file(username=os.environ['PLOTLY_USER'], api_key=os.environ['PLOTLY_PASS'])
plotly.tools.set_config_file(world_readable=True, sharing='public')

steel_last_price = []
steel_timestamp = []

for rec in collection.find({'item':'Steel'}):
    steel_last_price.append(rec['price'])
    steel_timestamp.append(datetime.datetime.fromtimestamp(rec['timestamp']))

steel_lp = Scatter(
    y=steel_last_price,
    x=steel_timestamp,
    name='Steel deals price',
    mode='lines+markers')

print(steel_lp)

data = [steel_lp]

layout = dict(
    title="Chat Wars Deals",
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label='1m',
                     step='month',
                     stepmode='backward'),
                dict(count=6,
                     label='6m',
                     step='month',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'
    )
)

fig = dict(data=data, layout=layout)
py.iplot(fig, filename = "Chat Wars Deals")

#plotly.offline.plot(
#    {
#        'data': data,
#        'layout': layout
#    },
#    filename=r"test.html", auto_open=True)