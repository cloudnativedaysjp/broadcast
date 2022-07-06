from obswebsocket import obsws, requests  # noqa: E402

class CreateScenes:
    # TODO: 実行中の操作を log として出すか、最後にチェックしたい
    def __init__(self, host, port, passwd):
        self.ws = obsws(host, port, passwd)
        self.ws.connect()
    def create_scenecollection(self, name):
        pass # v5 機能
        # 同名の SceneCollection が先にある場合はエラーを出す
    def create_scene(self, name):
        pass
    def create_source(self, kind, scenename, setting, visible):
        pass
        # ws.call(requests.CreateSource(f"{temp_scene_name}_temp_image_source_name", "image_source", temp_scene_name, None, None))
    def disconnect(self):
        self.ws.disconnect
