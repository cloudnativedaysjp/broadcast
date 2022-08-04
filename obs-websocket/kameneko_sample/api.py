import datetime
import logging
logger = logging.getLogger(__name__)
import string
import sys

import requests
import slackweb

import dk_token

track_list = {
    "A": 29,
    "B": 30,
    "C": 31
}

# デバッグ用
now = datetime.datetime.fromisoformat('2022-08-01T15:05:00.000+09:00')

def get_talks_5m(talks:list):
    
    within_5m = dict()
    # now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now_5m = now + datetime.timedelta(minutes=5)
    logger.debug("check time   : {}".format(now.time()))

    for talk in talks:
        start_time = datetime.datetime.fromisoformat(talk['startTime'])
        start_time_acutual = start_time + datetime.timedelta(minutes=talk['startOffset'])
        
        if (now_5m.time() >= start_time_acutual.time()) and (now.time() <= start_time_acutual.time()):
            logger.debug("title        : {}".format(talk['title']))
            logger.debug("trackid      : {}".format(talk['trackId']))
            logger.debug("now + 5m     : {}".format(now_5m.time()))
            logger.debug("session_time : {}".format(start_time_acutual.time()))
            
            within_5m = talk
            break
            
    return within_5m

def get_talks(DK_URL:string, token_path:string, track_id:int):
    if dk_token.check_dk_env(env_file_path=token_path):
        token = dk_token.read(env_file_path=token_path)
        req_url = "https://" + DK_URL + "/api/v1/talks/"
        
        params = {
            'eventAbbr': 'cnsec2022',
            'conferenceDayIds': 16,
            'trackId': str(track_id)
        }
        
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        
        logger.debug("url: {}header: {}".format(req_url, headers))
        res = requests.get(req_url, headers=headers, params=params)
        res_payload = res.json()
        
        return res_payload
    else:
        sys.exit()

def get_track_name(track_id:int):
    return [k for k, v in track_list.items() if v == track_id]
    
def get_track_id(track_name:string):
    return str(track_list[track_name])

def post_slack(message:string, webhook_url:string):
    slack = slackweb.Slack(url=webhook_url)
    slack.notify(text=message)
    
def post_slack_5m(talk_title:string, talk_track:string, webhook_url:string):
    message = """Track: `{}` で5分以内に次のセッションが開始します。
    OBSオペレーターはシーンのステータスを確認してください。確認が完了したら `:white_check_mark:` ( :white_check_mark: )リアクションをしてください。
    `{}`""".format(get_track_name(talk_track), talk_title)

    post_slack(message ,webhook_url)

def post_slack_90s(talk_title:string, talk_track:string, webhook_url:string):
    message = """Track: `{}` で1分30秒以内に次のセッションが開始します。
    `{}`""".format(get_track_name(talk_track), talk_title)

    post_slack(message ,webhook_url)

def post_slack_now(talk_title:string, talk_track:string, webhook_url:string):
    message = """Track: `{}` で次のセッションが開始しました。
    Dkの映像等が問題なければ `:white_check_mark:` ( :white_check_mark: )リアクションをしてください。
    `{}`""".format(get_track_name(talk_track), talk_title)

    post_slack(message ,webhook_url)

def check_talk_now(talk:dict):
    # now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    logger.debug("check time   : {}".format(now.time()))

    start_time = datetime.datetime.fromisoformat(talk['startTime'])
    start_time_acutual = start_time + datetime.timedelta(minutes=talk['startOffset'])
    
    if now.time() >= start_time_acutual.time():
        return True
    else:
        return False

def check_talk_90s(talk:dict):
    # now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
    now_90s = now + datetime.timedelta(seconds=90)
    logger.debug("check time   : {}".format(now.time()))

    start_time = datetime.datetime.fromisoformat(talk['startTime'])
    start_time_acutual = start_time + datetime.timedelta(minutes=talk['startOffset'])
    
    if (now_90s.time() > start_time_acutual.time()) and (now.time() < start_time_acutual.time()):
        return True
    else:
        return False