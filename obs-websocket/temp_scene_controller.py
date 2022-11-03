from ast import Pass
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
        self.MAKUAI_ID_FIRSTSESSION_INDEX = 1 # CSVで、Opening と Closing 等を除く最初のセッションが存在するインデックスを指定する(0始まり、ヘッダーは飛ばして数え始める)
        self.MAKUAI_ID_LASTSESSION_INDEX = 12 # CSVで、Opening と Closing 等を除く最後のセッションが存在するインデックスを指定する(0始まり、ヘッダーは飛ばして数え始める)
        self.MAKUAI_ID_INDEX_OFFSET = self.MAKUAI_ID_FIRSTSESSION_INDEX # CSVで、Opening と Closing 等を除く最初のセッションが存在するインデックスを指定する(0始まり、ヘッダーは飛ばして数え始める)

    async def create_scenes(self):
        await ws.connect() # Make the connection to obs-websocket
        await ws.wait_until_identified() # Wait for the identification handshake to complete

        requests = []

        # profile もいじって FHD にする

        requests.append(simpleobsws.Request('CreateSceneCollection', {'sceneCollectionName': f'{self.filename}'}))
        requests.append(simpleobsws.Request('CreateScene', {'sceneName': '調整中'}))
        requests.append(simpleobsws.Request('CreateInput', {'sceneName': "調整中", 'inputName':  "調整中_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/please_wait(調整中).mp4', 'looping': True}}))

        for i, session in enumerate(self.sessionsmodel.data):

            if session['title'] == '休憩': # CSV 内の休憩セッションは位置がちょっと都合が悪いので一度飛ばす。Opening の前後にも休憩がないといけないが、都合上ないため
                self.MAKUAI_ID_INDEX_OFFSET = self.MAKUAI_ID_INDEX_OFFSET + 1 # 幕間は セッションのみをカウントして 0,1,2~ と命名しているため
                continue

            # シーン・ソース追加
            ## 直前幕間シーン
            name = f"{session['id']}_{session['date'][8:10]}{session['track_id']}_〜{session['start_to_end'][0:5]}_休憩"
            requests.append(simpleobsws.Request('CreateScene', {'sceneName': f"{name}"}))
            ## 下に引く共通下地ロゴ画像 ソースを配置
            requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_休憩_base_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/蓋絵_white_00000.png'}}))
            # BGM を配置
            requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_bgm", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/Zac Nelson - Go with the Flow.mp3', 'looping': True}}))

            ### 幕間と CM の VLC ソースを配置
            if i < self.MAKUAI_ID_INDEX_OFFSET: # １本目の登壇より CSV 的に上にあるシーン(Opening など)
                ### Opening 直前幕間の VLC ソースを配置 (CM なし、 Tweet あり)
                if session['title']=='Opening':
                    pass #TODO: ←本番では外す
                    # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_makuai_media", 'inputKind': 'vlc_source', 'inputSettings': {'playlist': [{'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/幕間.mp4'}]}}))
                    # Twitter ウィジェット
                    # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_Twitter", 'inputKind': 'browser_source', 'inputSettings': {'height': 1080, 'is_local_file': True, 'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/twitter_hashtag/index.html', 'width': 1920}}))
                    # アスペクト比フィルター
                    # requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_makuai_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))
                    # ツイッターウィジェット位置設定 sceneItemId はハードコード
                    # requests.append(simpleobsws.Request('SetSceneItemTransform', {'sceneName': f"{name}", 'sceneItemId': 3, 'sceneItemTransform': {'alignment': 5, 'height': 568.0, 'positionX': 455.5, 'positionY': 1006.0, 'rotation': 0.0, 'scaleX': 0.5255208611488342, 'scaleY': 0.5259259343147278, 'sourceHeight': 1080.0, 'sourceWidth': 1920.0, 'width': 1009.0000610351562}}))
                    # TODO: 電光掲示板
            # elif i <= self.MAKUAI_ID_LASTSESSION_INDEX: # 通常の CFP 登壇 or スポンサーセッション
                # pass #TODO: ←本番では外す
                # makuai_id = i - self.MAKUAI_ID_INDEX_OFFSET
                # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_makuai_media", 'inputKind': 'vlc_source', 'inputSettings': {'playlist': [{'hidden': False, 'selected': False, 'value': f"/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/broadcast-{session['track_id']}/makuai/{makuai_id}.mp4"}, {'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/cm'}]}}))
                # # アスペクト比フィルター
                # requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_makuai_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))
            else: # closing や カンファレンス終了 の行など
                ### Closing 直前幕間の VLC ソースを配置 (CM なし、 Tweet あり)
                if session['title']=='Closing':
                    requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_makuai_media", 'inputKind': 'vlc_source', 'inputSettings': {'playlist': [{'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/幕間.mp4'}]}}))
                    # アスペクト比フィルター
                    requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_makuai_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))
                    # TODO: 電光掲示板
                    # Twitter ウィジェット
                    # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_Twitter", 'inputKind': 'browser_source', 'inputSettings': {'height': 1080, 'is_local_file': True, 'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/twitter_hashtag/index.html', 'width': 1920}}))
                    # ツイッターウィジェット位置設定 sceneItemId はハードコード
                    # requests.append(simpleobsws.Request('SetSceneItemTransform', {'sceneName': f"{name}", 'sceneItemId': 3, 'sceneItemTransform': {'alignment': 5, 'height': 568.0, 'positionX': 455.5, 'positionY': 1006.0, 'rotation': 0.0, 'scaleX': 0.5255208611488342, 'scaleY': 0.5259259343147278, 'sourceHeight': 1080.0, 'sourceWidth': 1920.0, 'width': 1009.0000610351562}}))

                ### Closing 後のエンドロール
                elif session['title']=='Observability Conference 2022は終了しました':
                    # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_休憩_ended_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/本日のイベントは終了しました.png'}}))
                    requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_休憩_ended_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/蓋絵_white_00000.png'}}))
                    # エンドロール向け VLC ソースを追加。カウントダウンは無し
                    # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'vlc_source', 'inputSettings': {'loop': False, 'playlist': [{'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/EndCredit.mp4'}]}}))
                    # Twitter ウィジェット
                    # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_Twitter", 'inputKind': 'browser_source', 'inputSettings': {'height': 1080, 'is_local_file': True, 'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/twitter_hashtag/index.html', 'width': 1920}}))
                    # アスペクト比フィルター
                    # requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))
                    # ツイッターウィジェット位置設定 sceneItemId はハードコード
                    # requests.append(simpleobsws.Request('SetSceneItemTransform', {'sceneName': f"{name}", 'sceneItemId': 4, 'sceneItemTransform': {'alignment': 5, 'height': 568.0, 'positionX': 455.5, 'positionY': 1006.0, 'rotation': 0.0, 'scaleX': 0.5255208611488342, 'scaleY': 0.5259259343147278, 'sourceHeight': 1080.0, 'sourceWidth': 1920.0, 'width': 1009.0000610351562}}))



            ## 登壇シーン
            name = f"{session['id']}_{session['date'][8:10]}{session['track_id']}_{session['start_to_end']}_{session['title'][0:16]}"
            requests.append(simpleobsws.Request('CreateScene', {'sceneName': f"{name}"}))
            ### 下に引く共通下地ロゴ画像 ソースを配置
            requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_base_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/蓋絵_white_00000.png'}}))


            ### 登壇向けメディアソース追加
            ## Opening
            if session['title']=='Opening':
                ### サイマル配信 from Studio1
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cndt2022-studio-a', 'is_local_file': False, 'restart_on_activate': False}}))
                # # オープニング向け VLC ソースを追加。カウントダウンは無し
                # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'vlc_source', 'inputSettings': {'loop': False, 'playlist': [{'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/Opening.mp4'}]}}))
                # アスペクト比フィルター
                requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))

            ## オンライン登壇
            elif session['presentation_method']=='オンライン登壇':

                ### RTMP メディアソースを追加
                #### CNDT2022Pre Event SY Studio 1 ( Track A )  SY Studio 2 ( Track B )
                if session['track_id']=='A':
                    requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cndt2022-a', 'is_local_file': False, 'restart_on_activate': False}}))
                elif session['track_id']=='B':
                    requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cndt2022-b', 'is_local_file': False, 'restart_on_activate': False}}))
                # アスペクト比フィルター
                requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))

            ## 事前収録
            elif session['presentation_method']=='事前収録':
                ### VLC ソースを追加
                escapedtitle = str(session['title']).replace('/', '_')
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media",  'inputKind': 'vlc_source', 'inputSettings': {'loop': False, 'playlist': [{'hidden': False, 'selected': True, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/CNDT2022_Countdown60.mp4'}, {'hidden': False, 'selected': False, 'value': f"/home/ubuntu/Nextcloud2/cndt2022-pre/{session['id']}_{escapedtitle}/{escapedtitle}.mp4"}]}}))
                # アスペクト比フィルター
                requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))

            ## 現地
            elif session['presentation_method']=='現地収録':
                # nginx studio (プレイベは)
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cndt2022-studio-a', 'is_local_file': False, 'restart_on_activate': False}}))
                # アスペクト比フィルター
                requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))

            ## Closing
            elif session['title']=='Closing':
                pass
                ### サイマル配信 from Studio1
                # requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cndt2022-a', 'is_local_file': False, 'restart_on_activate': False}}))
                # アスペクト比フィルター
                # requests.append(simpleobsws.Request('CreateSourceFilter', {'sourceName': f"{session['id']}_media", 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}))
                # TODO: 電光掲示板
                # TODO: Tweet ブラウザソース

            ## 終了画像 with BGM
            elif session['title']=='CNDT 2022は終了しました':
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  f"{session['id']}_ended_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/本日のイベントは終了しました.png'}}))
                requests.append(simpleobsws.Request('CreateInput', {'sceneName': f"{name}", 'inputName':  "main_bgm", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNDT2022/Sync/Media/z-common/Zac Nelson - Go with the Flow.mp3', 'looping': True}}))


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
# controller = TempSceneController('cnsec2022_2022-08-05_B.csv')
# controller = TempSceneController('cnsec2022_2022-08-05_C.csv')
# controller = TempSceneController('cndt2022_2022-11-01_A.csv')
controller = TempSceneController('cndt2022_2022-11-01_B.csv')

loop = asyncio.get_event_loop()
loop.run_until_complete(controller.create_scenes())
