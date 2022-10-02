import json
import logging
import time
import simpleobsws
import asyncio

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] [%(name)s] :%(message)s', filename="obsctl-robot.log")

import api
import obs
import dk_token

async def obs_init(ws):
    await ws.connect()
    await ws.wait_until_identified()

def main():
    talks = list()

    with open("secrets.json") as f:
        secret = json.loads(f.read())

        OBS_HOST= secret['obs']['host']
        OBS_PORT= secret['obs']['port']
        OBS_PASS= secret['obs']['password']
        DK_URL = secret['dreamkast']['url']
        DK_AUTH0_URL = secret['dreamkast']['url']
        DK_CLIENT_ID = secret['dreamkast']['client_id']
        DK_CLIENT_SECRETS = secret['dreamkast']['client_secrets']
        token_path = secret['token_path']
        webhook_url = secret['webhook_url']
        track_id = api.get_track_id(secret['track_name'])
        
        f.close()

    parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False)
    ws = simpleobsws.WebSocketClient(url = f'ws://{OBS_HOST}:{OBS_PORT}', password = OBS_PASS, identification_parameters = parameters)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(obs_init(ws))
    
    dk_token.get_token(DK_AUTH0_URL, DK_CLIENT_ID, DK_CLIENT_SECRETS)
    
    # 全体ループ
    while True:

        # 5分以内のセッション情報を取得
        while True:
            # セッション情報を取得
            # 新しい情報があれば既存のdictを更新
            talks_new:list = api.get_talks(DK_URL, token_path, track_id)
            if not talks == talks_new:
                talks = talks_new

            ready_talk:dict = api.get_talks_5m(talks)
            if ready_talk:
                break

            logger.debug("no talks after 5m")
            time.sleep(60)

        # 5分前のタイミングで通知
        api.post_slack_5m(ready_talk['title'], ready_talk['trackId'], webhook_url)
        
        # 1分半または時間になるまで1秒ずつ待つ
        while True:
            # 時間になったらSlackに通知してループを抜ける
            if api.check_talk_now(ready_talk):
                api.post_slack_now(ready_talk['title'], ready_talk['trackId'], webhook_url)
                break
            
            # 1分半前になったらSlackに通知
            elif api.check_talk_90s(ready_talk):
                api.post_slack_90s(ready_talk['title'], ready_talk['trackId'], webhook_url)
            
            time.sleep(1)
        
        # 切り替えたいシーンとアクティブシーンが同一でないなら切り替える
        if not loop.run_until_complete(obs.check_active_scene_identical(ws, ready_talk['id'])):
            loop.run_until_complete(obs.scene_change(ws, ready_talk['id']))
        
        # メディアソースの再生が開始して5秒待ってからチェックする
        # 再生開始直後は秒数がnullになることがあるため
        time.sleep(5)
        
        # メディアソースの残り時間が1分になるまで待つ
        while True:
            ms_time_left = loop.run_until_complete(obs.monitor_ms_time_left(ws, ready_talk['id']))
            logger.debug(ms_time_left)

            if ms_time_left <= 60:
                # 残り1分をSlackに通知
                message = """次のセッションが残り1分以内に終了します。
                `{}`""".format(ready_talk['title'])
                api.post_slack(message, webhook_url)
                break
            time.sleep(10)
        
        # メディアソースのステータスが OBS_MEDIA_STATE_ENDED になったら次のシーンへ切り替える
        while True:
            ms_state = loop.run_until_complete(obs.get_ms_play_state(ws, ready_talk['id']))
            logger.debug(ms_state)       
                
            if ms_state == "OBS_MEDIA_STATE_ENDED":
                loop.run_until_complete(obs.change_next_scene(ws))
                
                # 動画の終了をSlackに通知
                message = """次のセッションが終了しました。休憩シーンへ切り替えました。
                `{}`""".format(ready_talk['title'])
                api.post_slack(message, webhook_url)
                break
            
            time.sleep(1)
            
        logger.debug("ok")

if __name__ == "__main__":
    main()