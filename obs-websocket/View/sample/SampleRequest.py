import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
import os

HOST = os.environ["WSHOST"]
PORT = os.environ["WSPORT"]
PASS = os.environ["WSPASS"]

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

ws = simpleobsws.WebSocketClient(url = f'ws://{HOST}:{PORT}', password = PASS, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def make_request():
    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    # request = simpleobsws.Request('GetInputSettings', {'inputName': '画像 2'}) # Build a Request object
    request = simpleobsws.Request('CreateInput', {'sceneName': 'Opening', 'inputName': '画像 from Python', 'inputKind': 'image_source', '?inputSettings': {'file': '/Users/g.kunimi/Nextcloud2/Broadcast/CNSec2022/Sync/Media/z-common/蓋絵_white_00000.png'}}) # Build a Request object

    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly

loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())
