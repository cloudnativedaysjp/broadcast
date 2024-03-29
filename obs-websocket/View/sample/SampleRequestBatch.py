import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
import os

### バッチリクエストのサンプル https://github.com/IRLToolkit/simpleobsws/blob/master/samples/sample_request_batch.py

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

HOST = os.environ["WSHOST"]
PORT = os.environ["WSPORT"]
PASS = os.environ["WSPASS"]

ws = simpleobsws.WebSocketClient(url = f'ws://{HOST}:{PORT}', password = PASS, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request():
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    requests = []

    requests.append(simpleobsws.Request('GetVersion')) # Build a Request object, then append it to the batch
    requests.append(simpleobsws.Request('GetStats')) # Build another request object, and append it

    ret = await ws.call_batch(requests, halt_on_failure = False) # Perform the request batch

    for result in ret:
        if result.ok(): # Check if the request succeeded
            print("Request succeeded! Response data: {}".format(result.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly

loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())
