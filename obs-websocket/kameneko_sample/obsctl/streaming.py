import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
import asyncio
import simpleobsws
import os
import sys

# obsctl start streaming
async def start(ws):
    logging.debug("start_streaming()")

# obsctl stop streaming
async def stop(ws):
    logging.debug("stop_streaming()")