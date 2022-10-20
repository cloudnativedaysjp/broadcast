# export NEXTCLOUD_HOSTNAME="https://nextcloud.example.com:443"
# export NEXTCLOUD_ADMIN_USER="your_nextcloud_id"
# export NEXTCLOUD_ADMIN_PASSWORD="your_nextcloud_password"

import csv
import os

import urllib3
urllib3.disable_warnings()
from nextcloud import NextCloud

NEXTCLOUD_URL = os.environ.get('NEXTCLOUD_HOSTNAME')
NEXTCLOUD_USERNAME = os.environ.get('NEXTCLOUD_ADMIN_USER')
NEXTCLOUD_PASSWORD = os.environ.get('NEXTCLOUD_ADMIN_PASSWORD')
NEXTCLOUD_DIR_PATH = os.environ.get("/cndt2022/")
EVENT_TALK_FILE_PATH = os.environ.get("./cndt2022_all_all.csv")

talks = {}

talks = csv.DictReader(open(EVENT_TALK_FILE_PATH, encoding='utf_8', mode='r'))
print("id,title,speaker,url")

with NextCloud(
        NEXTCLOUD_URL,
        user=NEXTCLOUD_USERNAME,
        password=NEXTCLOUD_PASSWORD,
        session_kwargs={
            'verify': False
            }) as nxc:


    for talk in talks:
        dir_name = talk['id'] + "_" + talk['title']

        path = nxc.get_folder(path=NEXTCLOUD_DIR_PATH + dir_name.replace('/', '_'))['href'][27:-1]

        share_data = list(filter(lambda item : item['path'] == path, nxc.get_shares().data))
        share = ""

        if len(share_data) == 0:
            print("no share " + path)
            share = nxc.create_share(path=path, share_type=3, permissions=4).data
            nxc.update_share(sid=share['id'], permissions=4)
            print(talk['id'] + "," + talk['title'] + "," + talk['speaker'] + "," + share['url'])
        else:
            print("shared " + path + "(" + str(len(share_data)) + ")")
            share = share_data[0]