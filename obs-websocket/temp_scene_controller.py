import logging
# logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws
import os
import time

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
        self.sessionsmodel = SessionsModel(f"csv/{filename}") # 仮
        self.scenedata = None # TODO: ここで、 self.scenetmpl と self.sessions から作るべきシーンを dict に起こす
        self.MAKUAI_ID_FIRSTSESSION_INDEX = 2 # CSVで、最初のセッションが存在するインデックスを指定する(0始まり、ヘッダーは飛ばす)

    async def create_scenes(self):
        await ws.connect() # Make the connection to obs-websocket
        await ws.wait_until_identified() # Wait for the identification handshake to complete

        requests = []

        # profile もいじって FHD にする

        requests.append(simpleobsws.Request('CreateSceneCollection', {'sceneCollectionName': f'{self.filename}'}))
        requests.append(simpleobsws.Request('CreateScene', {'sceneName': '調整中'}))
        requests.append(simpleobsws.Request('CreateInput', {'sceneName': "調整中", 'inputName':  "調整中_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/please_wait(調整中).mp4', 'looping': True}}))
        requests.append(simpleobsws.Request('CreateInput', {'sceneName': "シーン", 'inputName':  "makuai_bgm", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Downloads/Hand In Hand Instrumental Version - Josh Leake.mp3', 'looping': True}}))
        requests.append(simpleobsws.Request('CreateInput', {'sceneName': "シーン", 'inputName':  "main_bgm", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Downloads/Possibilities - Josh Leake.mp3', 'looping': True}}))

        for i, session in enumerate(self.sessionsmodel.data):
            if session['title'] == '休憩': # CSV 内の休憩セッションは位置がちょっと都合が悪いので一度飛ばす。Opening の前後にも休憩がないといけないが、都合上ないため
                self.MAKUAI_ID_FIRSTSESSION_INDEX = self.MAKUAI_ID_FIRSTSESSION_INDEX + 1 # 幕間は セッションのみをカウントして 0,1,2~ と命名しているため
                continue

            # 直前幕間
            name = f"{session['id']}_{session['date'][8:10]}{session['track_id']}_〜{session['start_to_end'][0:5]}_休憩"
            requests.append(simpleobsws.Request('CreateScene', {'sceneName': f"{name}"}))
            # 下に引く蓋絵 ソースを配置
            requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_休憩_base_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/蓋絵_white_00000.png'}}))
            # 幕間と CM の VLC ソースを配置
            if i >= self.MAKUAI_ID_FIRSTSESSION_INDEX:
                makuai_id = i - self.MAKUAI_ID_FIRSTSESSION_INDEX
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_makuai_media", 'inputKind': 'vlc_source', 'inputSettings': {'playlist': [{'hidden': False, 'selected': False, 'value': f"/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/broadcast-{session['track_id']}/makuai/{makuai_id}.mp4"}, {'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/cm'}]}}))

            # 登壇シーン
            name = f"{session['id']}_{session['date'][8:10]}{session['track_id']}_{session['start_to_end']}_{session['title'][0:16]}"
            requests.append(simpleobsws.Request('CreateScene', {'sceneName': f"{name}"}))
            # 下に引く蓋絵 ソースを配置
            requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_base_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/蓋絵_white_00000.png'}}))

            if session['title']=='Opening':
                # オープニング向けサイマル RTMP ソースを追加
                # TODO: サイマルじゃなくて動画になりそう
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cnsec2022', 'is_local_file': False, 'restart_on_activate': False}}))

            if session['presentation_method']=='オンライン登壇':

                # RTMP メディアソースを追加

                # CNSec2022  SY Studio 1 ( Track A & B )  SY Studio 2 ( Track C )
                if session['track_id']=='A' or session['track_id']=='B':
                    requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cnsec2022', 'is_local_file': False, 'restart_on_activate': False}}))
                elif session['track_id']=='C':
                    requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx02.cloudnativedays.jp:10002/live/cnsec2022', 'is_local_file': False, 'restart_on_activate': False}}))

            elif session['presentation_method']=='事前収録':
                # VLC ソースを追加
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media",  'inputKind': 'vlc_source', 'inputSettings': {'loop': False, 'playlist': [{'hidden': False, 'selected': True, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/CNSec_Countdown60.mp4'}, {'hidden': False, 'selected': False, 'value': f"/home/ubuntu/Nextcloud2/cnsec2022/{session['id']}_{session['title']}/{session['title']}.mp4"}]}}))



            #TODO: closing 前の幕間が無いので良い感じにやる

        ret = await ws.call_batch(requests, halt_on_failure = True) # Perform the request batch

        for result in ret:
            if result.ok(): # Check if the request succeeded
                print("Request succeeded! Response data: {}".format(result.responseData))
            else:
                print(f" {result.requestType} Request Failed! 詳細: {result.requestStatus.comment}")


        # ソース
        # TODO: トランジションも追加して良い感じに

        await ws.disconnect() # Disconnect from the websocket server cleanly

# controller = TempSceneController('cnsec2022_2022-08-05_A.csv')
controller = TempSceneController('cnsec2022_2022-08-05_B.csv')
# controller = TempSceneController('cnsec2022_2022-08-05_C.csv')

loop = asyncio.get_event_loop()
loop.run_until_complete(controller.create_scenes())
