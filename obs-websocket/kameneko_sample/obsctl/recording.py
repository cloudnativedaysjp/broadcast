import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
import asyncio
import simpleobsws
import os
import sys

# obsctl start recording
async def start(ws):
    logging.debug("start_recording()")

# obsctl stop recording
async def stop(ws):
    logging.debug("stop_recording()")