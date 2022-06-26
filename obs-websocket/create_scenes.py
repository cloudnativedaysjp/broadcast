# -*- coding: utf-8 -*-

import sys
import time
import csv
import logging
import os
logging.basicConfig(level=logging.INFO)
sys.path.append('../')
from obswebsocket import obsws, requests  # noqa: E402

HOST = os.environ["WSHOST"]
PORT = 4444
PASS = os.environ["WSPASS"]

ws = obsws(HOST, PORT, PASS)
ws.connect()

temp_scene_names = ["temp_scene_1", "temp_scene_2", "temp_scene_3"]
temp_image_source_names = ["temp_image_source01"]

try:
    with open("/Users/g.kunimi/Documents/repos/github.com/cloudnativedaysjp/broadcast/obs-websocket/csv/cndt2021_2021-11-05_D.csv", encoding='utf8', newline='') as f:
        csvreader = csv.DictReader(f)
        for row in csvreader:
            temp_scene_name = row["start_to_end"] + "_" + row["title"]
            print(u"Creating {}".format(row['start_to_end']))
            ws.call(requests.CreateSource(f"{temp_scene_name}_temp_image_source_name", "image_source", temp_scene_name, None, None))
            time.sleep(2)
    #### ここで、既存のシーンを全消し? or Get でチェックして、冪等になるようにする ###
    # for temp_scene_name in temp_scene_names:
    #     print(u"Creating {}".format(temp_scene_name))
    #     ws.call(requests.CreateScene(temp_scene_name))
    #     time.sleep(2)
    #     for temp_image_source_name in temp_image_source_names:

    print("End of list")

except KeyboardInterrupt:
    pass

ws.disconnect()
