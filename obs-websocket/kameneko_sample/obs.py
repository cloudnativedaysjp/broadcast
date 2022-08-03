import asyncio
import datetime
import math
import logging
logger = logging.getLogger(__name__)
import simpleobsws
import logging
import sys

import api
    
async def scene_change(ws:simpleobsws, scene_id:int):
    request = simpleobsws.Request('GetSceneList')

    ret = await ws.call(request)
    if not ret.ok():
        logger.error("Request error. Request:{} Response:{}".format(request, ret))
        sys.exit()
    scenes = ret.responseData['scenes']
    
    request_scene_name = ""
    for scene in scenes:
        if scene['sceneName'].startswith(str(scene_id)):
            request_scene_name = scene['sceneName']
    if not request_scene_name:
        logger.error("request scene is not found. (id: {})".format(scene_id))

    request = simpleobsws.Request('SetCurrentProgramScene', {'sceneName': request_scene_name})

    ret = await ws.call(request)
    if not ret.ok():
        logger.error("Request error. \n  Request:{} \n  Response:{}".format(request, ret))
        sys.exit()
    
    logger.info("scene changed: {}".format(request_scene_name))

async def change_next_scene(ws):
    logger.debug("set_next()")

    request = simpleobsws.Request('GetSceneList')

    ret = await ws.call(request)
    if not ret.ok():
        logger.error("Request error. Request:{} Response:{}".format(request, ret))
        sys.exit()
    scenes = ret.responseData['scenes']
    logger.info(scenes)

    currentProgramSceneIndex =  [scene['sceneIndex'] for scene in scenes if scene['sceneName'] == ret.responseData['currentProgramSceneName']][0]
    currentProgramSceneName = ret.responseData['currentProgramSceneName']
    logger.info("current: [{}]{}".format(currentProgramSceneIndex, currentProgramSceneName))

    nextSceneIndex = currentProgramSceneIndex - 1
    if nextSceneIndex < 0:
        logger.info("current scene is tha last scene.")
    else:
        logger.info("nextScene: [{}]{}".format(nextSceneIndex, scenes[nextSceneIndex]))

    request = simpleobsws.Request('SetCurrentProgramScene', {'sceneName': scenes[nextSceneIndex]['sceneName']})

    ret = await ws.call(request)
    if not ret.ok():
        logger.error("Request error. \n  Request:{} \n  Response:{}".format(request, ret))
        sys.exit()

async def check_active_scene_identical(ws:simpleobsws, talk_id:int):
    request = simpleobsws.Request('GetSceneList')

    ret = await ws.call(request)
    if not ret.ok():
        logger.error("Request error. Request:{} Response:{}".format(request, ret))
        sys.exit()
    scenes = ret.responseData['scenes']
    
    request_scene_name = ""
    for scene in scenes:
        if scene['sceneName'].startswith(str(talk_id)):
            request_scene_name = scene['sceneName']
        
    logger.debug(ret)
    current_scene_name = ret.responseData['currentProgramSceneName']
    logger.debug("current scene: {}".format(current_scene_name))
    logger.debug("request scene: {}".format(request_scene_name))
    
    if current_scene_name == request_scene_name:
        logger.debug("active scene is request scene")
        return True
    else:
        return False

async def monitor_ms_time_left(ws:simpleobsws, talk_id:int):
    source_name = "{}_media".format(talk_id)

    logger.debug("get_mediasource_time({})".format(source_name))
    request = simpleobsws.Request('GetMediaInputStatus', {'inputName': source_name})

    ret = await ws.call(request)
    if ret.ok():
        cursor = datetime.timedelta(milliseconds=ret.responseData['mediaCursor'])
        duration = datetime.timedelta(milliseconds=ret.responseData['mediaDuration'])
        
        return duration.total_seconds() - cursor.total_seconds()

    else:
        logger.error("failed mediasource")


async def get_ms_play_state(ws:simpleobsws, talk_id:int):
    source_name = "{}_media".format(talk_id)

    logger.debug("get_mediasource_time({})".format(source_name))
    request = simpleobsws.Request('GetMediaInputStatus', {'inputName': source_name})

    ret = await ws.call(request)
    if ret.ok():
        state = ret.responseData['mediaState']
        
        return state

    else:
        logger.error("failed mediasource")
