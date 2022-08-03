

import datetime
import json
import logging
logger = logging.getLogger(__name__)
import os
import sys

import jwt
import requests


def read(env_file_path):
    token_file = open(env_file_path, "r")
    token = token_file.read()
    token_file.close()

    return token

def check_dk_env(env_file_path):
    if os.path.isfile(env_file_path):
        token = read(env_file_path=env_file_path)
    else:
        logger.error("The '{}' not found.'".format(env_file_path))
        return False
    
    token_payload = jwt.decode(token, options={"verify_signature": False})
    token_expire = datetime.datetime.fromtimestamp(token_payload['exp'])

    if datetime.datetime.now() < token_expire:
        return True
    else:
        logger.info("The token is expired.")
        return False

def get_token(DK_AUTH0_URL, DK_CLIENT_ID, DK_CLIENT_SECRETS):
    env_file_path = ".token"

    if check_dk_env(env_file_path=env_file_path):
        logger.info("token not expired")
    else:
        req_url = "https://" + DK_AUTH0_URL + "/oauth/token"
        headers = {
            "content-type": "application/json"
        }
        data = {
            "client_id":"",
            "client_secret":"",
            "audience":"https://event.cloudnativedays.jp/",
            "grant_type":"client_credentials"
        }
        data['client_id'] = DK_CLIENT_ID
        data['client_secret'] = DK_CLIENT_SECRETS

        res = requests.post(req_url, headers=headers, data=json.dumps(data))
        res_payload = res.json()
        logger.info("token update successfully ({})".format(res_payload))

        token_file = open(".token", "w")
        token_file.write(res_payload['access_token'])
        token_file.close()