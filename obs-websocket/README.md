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


## ソース (input) を作成する
GetInputSettings でパラメータの入れ方を取得して、 CreateInput の inputSettings に指定すると良さそう

| ソース名 | CreateInput の Data 一例|
| --- | --- |
| 画像 | {'sceneName': "Opening", 'inputName':  "Opening_base_image", 'inputKind': 'image_source', 'inputSettings': {'file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/蓋絵_white_00000.png'}} |
| メディアソース (ループあり) | {'sceneName': "Opening", 'inputName':  "Opening_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/幕間.mp4', 'looping': True}} |
| 幕間用 vlc ソース (幕間動画->イベントPR->CMディレクトリ)(ループあり)| {'sceneName': "Opening", 'inputName':  "Opening_vlc", 'inputKind': 'vlc_source', 'inputSettings': {'playlist': [{'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/broadcast-B/makuai/0.mp4'},  {'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/cm'}]}} |
| 登壇用 RTMP メディアソース | {'sceneName': "Opening", 'inputName':  "RTMP_media", 'inputKind': 'ffmpeg_source', 'inputSettings': {'buffering_mb': 0, 'input': 'rtmp://nginx01.cloudnativedays.jp:10002/live/cnsec2022', 'is_local_file': False, 'restart_on_activate': False}}
| 収録動画用 vlc ソース (カウントダウン->登壇動画)(ループ無し) | {'sceneName': "Opening", 'inputName':  "1451_media", 'inputKind': 'vlc_source', 'inputSettings': {'loop': False, 'playlist': [{'hidden': False, 'selected': True, 'value': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/CNSec_Countdown60.mp4'}, {'hidden': False, 'selected': False, 'value': '/home/ubuntu/Nextcloud2/cnsec2022/1451_実践 SpiceDB - クライドネイティブ時代をサバイブできるパーミッション管理の実装を目指して/実践 SpiceDB - クラウドネイティブ時代をサバイブできるパーミッション管理の実装を目指して.mp4'}]}}
| ブラウザソース(Twitter巡回) | {'sceneName': "Opening", 'inputName':  "Twitter", 'inputKind': 'browser_source', 'inputSettings': {'height': 1080, 'is_local_file': True, 'local_file': '/home/ubuntu/Nextcloud/Broadcast/CNSec2022/Sync/Media/z-common/twitter_hashtag/index.html', 'width': 1920}}|

## 既存のソースをシーンに追加する
CreateSceneItem

## フィルターをソースに追加する
| フィルター名 | CreateSourceFilter の一例 |
| --- | --- |
| アスペクト比 | {'sourceName': '1466_makuai_media', 'filterName': 'スケーリング/アスペクト比', 'filterKind': 'scale_filter', 'filterSettings': {'resolution': '1920x1080'}}

## ソースの位置を設定する
| 例 | SetSceneItemTransform |
| --- | --- |
| - | {'sceneName': dvdStageSceneName, 'sceneItemId': sceneItemId,  'sceneItemTransform': {'alignment': 5, 'boundsAlignment': 0, 'boundsHeight': 0.0, 'boundsType': 'OBS_BOUNDS_NONE', 'boundsWidth': 0.0, 'cropBottom': 0, 'cropLeft': 0, 'cropRight': 0, 'cropTop': 0, 'height': 568.0, 'positionX': 455.5, 'positionY': 1006.0, 'rotation': 0.0, 'scaleX': 0.5255208611488342, 'scaleY': 0.5259259343147278, 'sourceHeight': 1080.0, 'sourceWidth': 1920.0, 'width': 1009.0000610351562}|
