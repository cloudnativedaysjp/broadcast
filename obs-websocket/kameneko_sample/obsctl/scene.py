import logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
import asyncio
import simpleobsws
import os
import sys

# obsctl scene get
async def get(ws):
    request = simpleobsws.Request('GetSceneList')

    ret = await ws.call(request)
    if not ret.ok():
        logging.error("Request error. Request:{} Response:{}".format(request, ret))
        sys.exit()
    scenes = ret.responseData['scenes']
    print(ret)

    for scene in reversed(scenes):
        logging.info("scene[{}]: {}".format(scene['sceneIndex'], scene['sceneName']))

    currentProgramSceneIndex = next((x for x in ret.responseData['scenes'] if x['sceneName'] == ret.responseData['currentProgramSceneName']), None)['sceneIndex']
    currentProgramSceneName = ret.responseData['currentProgramSceneName']
    logging.info("current: [{}]{}".format(currentProgramSceneIndex, currentProgramSceneName))

    nextSceneIndex = currentProgramSceneIndex - 1
    if nextSceneIndex < 0:
        logging.info("current scene is tha last scene.")
    else:
        logging.info("nextScene: [{}]{}".format(nextSceneIndex, scenes[nextSceneIndex]))

# obsctl scene next
async def next(ws):
    logging.debug("set_next()")

# obsctl scene set {sceneName}
async def set(ws, sceneName):
    logging.debug("set_scene({})".format(sceneName))