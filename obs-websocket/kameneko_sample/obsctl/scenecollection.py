import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
import asyncio
import simpleobsws
import os
import sys

# obsctl get scenecollection
async def get(ws):
    logging.debug("get_scenecollection()")