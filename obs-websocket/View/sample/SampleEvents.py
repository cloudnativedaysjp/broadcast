import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
import os

### コネクション試験などに使えるサンプル https://github.com/IRLToolkit/simpleobsws/blob/master/samples/sample_events.py

parameters = simpleobsws.IdentificationParameters() # Create an IdentificationParameters object
parameters.eventSubscriptions = (1 << 0) | (1 << 2) # Subscribe to the General and Scenes categories

HOST = os.environ["WSHOST"]
PORT = os.environ["WSPORT"]
PASS = os.environ["WSPASS"]

ws = simpleobsws.WebSocketClient(url = f'ws://{HOST}:{PORT}', password = PASS, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def on_event(eventType, eventData):
    print('New event! Type: {} | Raw Data: {}'.format(eventType, eventData)) # Print the event data. Note that `update-type` is also provided in the data

async def on_switchscenes(eventData):
    print('Scene switched to "{}".'.format(eventData['sceneName']))

async def init():
    await ws.connect()
    await ws.wait_until_identified()

loop = asyncio.get_event_loop()
loop.run_until_complete(init())
ws.register_event_callback(on_event) # By not specifying an event to listen to, all events are sent to this callback.
ws.register_event_callback(on_switchscenes, 'SwitchScenes')
loop.run_forever()
