import json

class SceneTmplModel:
    def __init__(self) :
        self.data = None
        # TODO: ディレクトリ内を走査して presentation_method 毎のテンプレートを読む
        with open("Model/tmpl/事前収録.json", 'r') as f:
            self.data = json.load(f)
