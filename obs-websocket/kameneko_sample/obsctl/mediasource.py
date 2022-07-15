import logging
import asyncio
import simpleobsws
import os
import sys
import json
import datetime
import time

async def get(ws):
    logging.debug("set_mediasource()")

# obsctl get mediasource time {mediasourceName}
async def time(ws, mediasourceName):
    logging.debug("get_mediasource_time({})".format(mediasourceName))
    while True:
        request = simpleobsws.Request('GetMediaInputStatus', {'inputName': mediasourceName})

        ret = await ws.call(request) # Perform the request
        if ret.ok(): # Check if the request succeeded
            state = ret.responseData['mediaState']
            cursor = datetime.timedelta(milliseconds=ret.responseData['mediaCursor'])
            duration = datetime.timedelta(milliseconds=ret.responseData['mediaDuration'])
            cursor_parcent = (cursor / duration) * 100
            print("\r[{}]: {:.1f}% | {} / {}".format(state, cursor_parcent, cursor, duration), end="")
            # time.sleep(1)
