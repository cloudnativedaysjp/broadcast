import csv

class SessionsModel:
    def __init__(self, filename) :
        self.data = None
        self.filename = filename
        # TODO: ディレクトリ内を走査して トラック 毎の csv を読む
        with open(filename, 'r') as f:
            self.data = csv.DictReader(f)
