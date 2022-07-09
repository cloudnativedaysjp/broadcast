import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
import os

from Model.SceneTmplModel import SceneTmplModel
from Model.SessionsModel import SessionsModel


### バッチリクエストのサンプルをもとに、一旦すべてハードコードで作る

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

HOST = os.environ["WSHOST"]
PORT = os.environ["WSPORT"]
PASS = os.environ["WSPASS"]

ws = simpleobsws.WebSocketClient(url = f'ws://{HOST}:{PORT}', password = PASS, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

class TempSceneController:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.scenetmpl = SceneTmplModel()
        self.sessionsmodel = SessionsModel(f"csv/{filename}.csv") # 仮
        self.scenedata = None # TODO: ここで、 self.scenetmpl と self.sessions から作るべきシーンを dict に起こす

    async def create_scenes(self):
        await ws.connect() # Make the connection to obs-websocket
        await ws.wait_until_identified() # Wait for the identification handshake to complete

        requests = []

        # profile もいじって FHD にする

        requests.append(simpleobsws.Request('CreateSceneCollection', {'sceneCollectionName': f'{self.filename}'}))
        requests.append(simpleobsws.Request('CreateScene', {'sceneName': '調整中'}))
        requests.append(simpleobsws.Request('CreateScene', {'sceneName': '待機ループ'}))
        for session in self.sessionsmodel.data:
            name = f"{self.sessionsmodel.filename[-8:-4]}-{session['start_to_end']}-{session['title'][0:8]}"
            requests.append(simpleobsws.Request('CreateScene', {'sceneName': f"{name}"}))
        requests.append(simpleobsws.Request('CreateScene', {'sceneName': 'closing 前待機ループ'}))
        requests.append(simpleobsws.Request('CreateScene', {'sceneName': 'closing'}))

        # ソース

        ret = await ws.call_batch(requests, halt_on_failure = False) # Perform the request batch

        for result in ret:
            if result.ok(): # Check if the request succeeded
                print("Request succeeded! Response data: {}".format(result.responseData))
            else:
                print(f" {result.requestType} Request Failed! 詳細: {result.requestStatus.comment}")

        await ws.disconnect() # Disconnect from the websocket server cleanly

controller = TempSceneController('cnsec2022_2022-07-12_A')
# controller = TempSceneController('cnsec2022_2022-07-12_B')

loop = asyncio.get_event_loop()
loop.run_until_complete(controller.create_scenes())
