import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
import asyncio
import simpleobsws
import os
import sys
# obsctl get source {sceneName}
async def get(ws, sceneName):
    logging.debug("get_source({})".format(sceneName))
