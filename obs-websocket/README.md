## 使い方

1. dreamkast 管理画面の tracks タブから、CSV をダウンロードする
2. `obs-websocket/csv` 以下に配置する
3. TODO:

## 環境変数

  | KEY | VALUE |
  |---|---|
  | WSHOST | 操作対象のOBSの IP アドレス |
  | WSPASS | 操作対象のOBSの OBS-WebSocket の パスワード|
  | WSPORT | 操作対象のOBSの OBS-WebSocket の ポート番号|

(memo) windows で wsl2 を使って開発しながら、同じ windows マシンの OBS に接続する場合は以下のコマンドで出力される IP を WSHOST に指定する。 [参考](https://qiita.com/samunohito/items/019c1432161a950892be)
```bash
ip route | grep 'default via' | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
```

## 要件
- Python >= 3.7  を接続元マシンに導入していること
- obs-websocket >= **5.0.0** を接続先 OBS に導入していること
