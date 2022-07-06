## 使い方

1. dreamkast 管理画面の tracks タブから、CSV をダウンロードする
2. `obs-websocket/csv` 以下に配置する

## 環境変数

  | KEY | VALUE |
  |---|---|
  | WSHOST | 操作対象のOBSの IP アドレス |
  | WSPASS | 操作対象のOBSの OBS-WebSocket の パスワード|

(memo) windows で wsl2 を使って開発しながら、同じ windows マシンの OBS に接続する場合は以下のコマンドで出力される IP を WSHOST に指定する。 [参考](https://qiita.com/samunohito/items/019c1432161a950892be)
```bash
ip route | grep 'default via' | grep -Eo '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'
```

## 要件
- python3
- obs-websocket を 接続先 OBS に導入していること
