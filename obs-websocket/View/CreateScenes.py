import logging
logging.basicConfig(level=logging.DEBUG)
import asyncio
import simpleobsws

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)

class CreateScenes:
    async def __init__(self, host, port, passwd):
        self.ws = simpleobsws.WebSocketClient(url = f'ws://{host}:{port}', password = passwd, identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.
        await self.ws.connect()
        await self.ws.wait_until_identified() # Wait for the identification handshake to complete

    async def create_scenecollection(self, name):
        pass # v5 機能
        # 同名の SceneCollection が先にある場合はエラーを出す

    async def create_scene(self, data):
        pass
        requests = []
        requests.append(simpleobsws.Request('GetVersion')) # Build a Request object, then append it to the batch
        requests.append(simpleobsws.Request('GetStats')) # Build another request object, and append it
        ret = await self.ws.call_batch(requests, halt_on_failure = False) # Perform the request batch

    async def create_source(self, kind, scenename, setting, visible):
        pass
        # ws.call(requests.CreateSource(f"{temp_scene_name}_temp_image_source_name", "image_source", temp_scene_name, None, None))

    async def disconnect(self):
        self.ws.disconnect()
