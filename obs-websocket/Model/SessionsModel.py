import csv

class SessionsModel:
    def __init__(self, filename) :
        self.data = None
        self.filename = filename
        # TODO: ディレクトリ内を走査して トラック 毎の csv を読む
        self.f = open(filename, 'r')
        self.data = csv.DictReader(self.f)
    def __del__(self):
        self.f.close() # これでいいのかは不明 with open だと インスタンスから .data にアクセスしたときに I/O operation on closed file. となる

