# -*- coding: utf-8 -*-

# エントリポイント/Controller
import os

import Model
from Model.SceneTmplModel import SceneTmplModel
from Model.SessionsModel import SessionsModel

import View
from View.CreateScenes import CreateScenes

HOST = os.environ["WSHOST"]
PORT = 4444
PASS = os.environ["WSPASS"]

class CreateScenesController:
    def __init__(self) -> None:
        self.scenetmpl = SceneTmplModel()
        self.sessions = SessionsModel("csv/o11y2022_2022-03-11_A.csv") # 仮
        self.createscene = CreateScenes(HOST, PORT, PASS)

    def run(self):
        self.createscene.create_scenecollection(self.sessions.filename)
        # template から


if __name__ == "__main__":
    createscenescontroller = CreateScenesController()
    createscenescontroller.run()
    createscenescontroller.createscene.disconnect()
