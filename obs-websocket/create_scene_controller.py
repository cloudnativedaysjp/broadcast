# -*- coding: utf-8 -*-

# エントリポイント/Controller
import os

from Model.SceneTmplModel import SceneTmplModel
from Model.SessionsModel import SessionsModel

from View.CreateScenes import CreateScenes

HOST = os.environ["WSHOST"]
PORT = os.environ["WSPORT"]
PASS = os.environ["WSPASS"]

class CreateScenesController:
    def __init__(self) -> None:
        self.scenetmpl = SceneTmplModel()
        self.sessions = SessionsModel("csv/o11y2022_2022-03-11_A.csv") # 仮
        self.createscene = CreateScenes(HOST, PORT, PASS)
        self.scenedata = None # TODO: ここで、 self.scenetmpl と self.sessions から作るべきシーンを dict に起こす

    def run(self):
        self.createscene.create_scenecollection(self.sessions.filename)
        # template から batch リクエストを作成してシーンを構築する
        self.createscene.create_scene(self.scenedata)


if __name__ == "__main__":
    createscenescontroller = CreateScenesController()
    createscenescontroller.run()
    createscenescontroller.createscene.disconnect()
