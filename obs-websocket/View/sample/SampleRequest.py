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

    # request = simpleobsws.Request('GetSourceFilter', {'sourceName': '1468_media',  'filterName': 'スケーリング/アスペクト比'}) # Build a Request object
    # request = simpleobsws.Request('GetInputSettings', {'inputName': 'テキスト'}) # Build a Request object
    # request = simpleobsws.Request('GetSceneItemId', {'sceneName': "1485_05A_〜13:00_休憩", 'sourceName': "ブラウザ"}) # Build a Request object
    # request = simpleobsws.Request('GetSceneItemTransform', {'sceneName': "1485_05A_〜13:00_休憩", 'sceneItemId': 3}) # Build a Request object
    request = simpleobsws.Request('SetSceneItemTransform', {'sceneName': "1485_05A_〜13:00_休憩", 'sceneItemId': 3, 'sceneItemTransform': {'alignment': 5, 'height': 568.0, 'positionX': 455.5, 'positionY': 1006.0, 'rotation': 0.0, 'scaleX': 0.5255208611488342, 'scaleY': 0.5259259343147278, 'sourceHeight': 1080.0, 'sourceWidth': 1920.0, 'width': 1009.0000610351562}}) # Build a Request object
    # request = simpleobsws.Request('CreateInput', {'sceneName': 'Opening', 'inputName': '画像 from Python setting', 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/蓋絵_white_00000.png'}}) # Build a Request object
    # request = simpleobsws.Request('CreateInput', {'sceneName': "Opening", 'inputName':  "Opening_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/幕間.mp4', 'looping': True}}) # Build a Request object

    ret = await ws.call(request) # Perform the request
    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))

    await ws.disconnect() # Disconnect from the websocket server cleanly

loop = asyncio.get_event_loop()
loop.run_until_complete(make_request())
