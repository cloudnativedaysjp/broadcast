# -*- coding: utf-8 -*-

import sys
import time
import os

import logging
logging.basicConfig(level=logging.INFO)

sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

HOST = os.environ["WSHOST"]
PORT = 4444
PASS = os.environ["WSPASS"]

ws = obsws(HOST, PORT, PASS)
ws.connect()

try:
    scenes = ws.call(requests.GetSceneList())
    for s in scenes.getScenes():
        name = s['name']
        print(u"Switching to {}".format(name))
        ws.call(requests.SetCurrentScene(name))
        time.sleep(2)

    print("End of list")

except KeyboardInterrupt:
    pass

ws.disconnect()
