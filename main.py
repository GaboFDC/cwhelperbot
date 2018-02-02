#!/usr/bin/env python
# coding=utf-8

from flask import Flask, render_template, request
from config import *
from time import sleep

app = Flask(__name__)
# app.config.from_pyfile('flaskapp.cfg')


@app.route('/')
def index():
    return render_template('index.html')


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()
sleep(1) # Avoid timeout

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=APP_PORT,
        debug=True)
