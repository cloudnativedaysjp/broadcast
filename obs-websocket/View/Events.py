#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
import os

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, events  # noqa: E402

HOST = os.environ["WSHOST"]
PORT = 4444
PASS = os.environ["WSPASS"]

def on_event(message):
    print(u"Got message: {}".format(message))


def on_switch(message):
    print(u"You changed the scene to {}".format(message.getSceneName()))


ws = obsws(HOST, PORT, PASS)
ws.register(on_event)
ws.register(on_switch, events.SwitchScenes)
ws.connect()

try:
    print("OK")
    time.sleep(10)
    print("END")

except KeyboardInterrupt:
    pass

ws.disconnect()
