media checker
=============

指定のフォルダにアップロードされた事前収録動画の自動チェックを行います。

## Prerequisites
- Python3
  - pytz
  - PyJWT
- ffmpeg
- jq

以下のバージョンで動作検証済み。
```bash
$ python3 --version
Python 3.8.10

$ pip3 list
...
pytz 2022.1
PyJWT 1.7.1
...

$ ffmpeg -version
ffmpeg version 4.2.7-0ubuntu0.1 Copyright (c) 2000-2022 the FFmpeg developers
built with gcc 9 (Ubuntu 9.4.0-1ubuntu1~20.04.1)

$ jq --version
jq-1.6
```

## Usage
```bash
$ python3 media_checker.py --help

usage: media_checker.py [-h] {put,stdout} ...

動画の情報を取得し、判定条件を満たしているか否かを判定する

positional arguments:
  {put,stdout}
    put         セッションの最新ファイルごとに動画のチェック結果をDkにAPI経由で連携する
    stdout      指定のディレクトリ配下の全ての動画の情報を標準出力する

optional arguments:
  -h, --help    show this help message and exit
```

### media_checker.py put
セッションの最新ファイルごとに動画のチェックを行いその結果をDkにAPI経由で連携します。

セッション動画格納先のROOTディレクトリとセッションリストのCSVを指定し、CSVに記載のあるセッション毎に動画が格納されている場合にチェックを行います。  
セッションフォルダに複数の動画が存在する場合には、タイムスタンプが最新の動画のみを規定に沿うかチェックし音量の規格化を行う。  
その後csvファイルに記載のセッション名にrenameします。

```bash
$ python3 media_checker.py put --help

usage: media_checker.py put [-h] --csv CSV_FILE --upper_limit DURATION_UPPER_LIMIT --lower_limit DURATION_LOWER_LIMIT

optional arguments:
  -h, --help            show this help message and exit
  --csv CSV_FILE        セッションのCSVリスト
  --upper_limit DURATION_UPPER_LIMIT
                        動画の長さの上限の指定(分)
  --lower_limit DURATION_LOWER_LIMIT
                        動画の長さの下限の指定(分)
```

Slack通知は、以下のタイミングで行われます。
| 契機 | 挙動 |
| :-- | :-- |
| 環境変数(TOKEN/DREAMKAST_DOMAIN)が確認できない場合 | Dk連携に必要な環境変数が確認できない場合に通知し、処理を終了する |
| Dk連携できない場合 | DkへのPUTが失敗した場合に通知し、処理を終了する |
| 動画情報の取得に失敗した場合 | Dk通知用の動画情報の取得に失敗した場合に通知し、次の動画ファイルの処理に移る |

### media_checker.py stdout
指定したセッション動画格納先のROOTディレクトリ配下に格納されている全ての動画情報を標準出力します。

```bash
$ python3 media_checker.py stdout --help

usage: media_checker.py stdout [-h] --upper_limit DURATION_UPPER_LIMIT --lower_limit DURATION_LOWER_LIMIT

optional arguments:
  -h, --help            show this help message and exit
  --upper_limit DURATION_UPPER_LIMIT
                        動画の長さの上限の指定(分)
  --lower_limit DURATION_LOWER_LIMIT
                        動画の長さの下限の指定(分)
```

## How to Setup to put method
`put method` は、`cron`にてX分おきに実行することを想定しています。  

スクリプトと同じディレクトリに配置されている変数ファイル(media_checker_env.json)を参照します。
media_checker_env.json 内の変数をあらかじめ更新してください。  
`<CLIENT ID>`, `<CLIENT_SECRET>`に関しては、[DreamkastのREADME](https://github.com/cloudnativedaysjp/dreamkast#how-to-use-rest-api-for-videoregistration)を参照のこと。

また、**JWT Token発行数には月上限が存在するため、必要以上の実行をしないよう留意する。**

**media_checker.py put**
下記形式でcronをセットする。
```
python3 <SCRIPT DIR>/media_checker.py put --upper_limit "XX" --lower_limit "YY" --csv "<PATH TO CSV>"
```

例えば、下記のようなディレクトリ構造の場合 かつ 動画の長さの判定基準が 20 ~ 45分の場合
```
<ROOT FOLDER OF MEDIAS>
  ﹂ /uploads/
      ﹂ 0000_session01/
          ﹂ session01.mp4
      ﹂ 1111_session02
          ﹂ session02.mp4
  ﹂ media_checker.py
  ﹂ env_set.sh
  ﹂ <CSV FILE>
  ﹂ <ENV FILE>
```

cronの設定は以下のようになる
```bash
# cronjob for media_checker.py
*/5 * * * * python3 <ROOT FOLDER OF MEDIAS>/media_checker.py put --upper_limit "45" --lower_limit "20" --csv "<CSV FILE>"
```


## 取得される動画情報
動画情報は下記のフォーマットで取得されます。
```
{
  "status": "confirmed",
  "statistics": {
            "ファイル名": "XX.mp4",
            "チェック日時": "YYYY/MM/DD hh:mm:ss",
            "解像度チェック": "OK",
            "解像度タイプ": "FHD",
            "アスペクト比チェック": "OK",
            "アスペクト比": "16:9",
            "動画の長さチェック": "OK",
            "動画の長さコメント": "OK",
            "ファイルサイズチェック": "OK",
            "ファイルサイズコメント": "OK"
          }
}
```

| Item | Description |
| :--  | :--  |
| status | `confirmed` or `invalid_format`、<br/>全てのチェックがOKの場合に`confirmed`、それ以外の場合に`invalid_format`を返却 |
| ファイル名 | CSVに記載のセッション名.mp4 |
| チェック日時 | 動画のチェックを行った時間(JST) |
| 解像度チェック | 指定した解像度タイプに合致する場合 `OK`、それ以外の場合に`NG` |
| 解像度タイプ | `target_ratio`で指定する。<br/>`target_ratio`自体は`require_resolutions[X]["ratio"]` の `X`で判定する解像度を指定<br/> 0: SD, 1: HD, 2: FullHD, 3:  WQHD, 4: 4K|
| アスペクト比チェック | 指定したアスペクト比に合致する場合 `OK`、それ以外の場合に`NG` |
| アスペクト比 | `vertical_criteria_ratio`(横)と `horizontal_criteria_ratio`(縦)で指定した比率であれば、指定したアスペクト比を返却<br/>合致しない場合は動画の`横幅×縦幅`の数値を返却 |
| 動画の長さのチェック | 動画の長さが指定した範囲内であれば`OK`、逸脱している場合に`NG` |
| 動画の長さコメント | 動画の長さの上限下限は、スクリプトの引数で指定する<br/>- 下限を下回る場合: 基準値（XX分）を下回っています <br>- 上限下限に収まっている場合: 適切な動画の長さです <br>- 上限を超えている場合: 基準値（XX分）を超えています |
| ファイルサイズチェック | `size_flag` = `True`の場合に出力される<br/>動画の容量上限を超えていなければ`OK`、超えている場合は`NG` |
| ファイルサイズコメント | 動画の容量上限(MB)は`size_upper_limit`で指定する(デフォルト2000MB)<br>- 上限内の場合: 基準値内の動画サイズです<br/>- 上限を超過している場合: 基準値（YY MB）を超えています |

スクリプト内で編集可能なオプションは以下
```bash
# Default criterion
# Target ratio
target_ratio = require_resolutions[2]["ratio"]
horizontal_criteria_ratio = 16
vertical_criteria_ratio = 9

# Target file size(MiB)
size_upper_limit = 2000
size_flag = True
```

## Example
- FullHD、問題なし
```
{
  "status": "confirmed",
  "statistics": {
            "ファイル名": "XX.mp4",
            "チェック日時": "2022-07-14 20:55:23",
            "解像度チェック": "OK",
            "解像度タイプ": "FHD",
            "アスペクト比チェック": "OK",
            "アスペクト比": "16:9",
            "動画の長さチェック": "OK",
            "動画の長さコメント": "OK",
            "ファイルサイズチェック": "OK",
            "ファイルサイズコメント": "OK"
          }
}
```

- エラー時
```
{
  "status": "invalid_format",
  "statistics": {
            "ファイル名": "XX.mp4",
            "チェック日時": "2022-07-14 20:55:23",
            "解像度チェック": "NG",
            "解像度タイプ": "Non Standard",
            "アスペクト比チェック": "NG",
            "アスペクト比": "1728 x 1080",
            "動画の長さチェック": "NG",
            "動画の長さコメント": "基準値（20分）を超えています",
            "ファイルサイズチェック": "NG",
            "ファイルサイズコメント": "基準値（2GB）を超えています"
          }
}
```

- MP4以外がアップロードされた場合
```
{
  "status": "invalid_format",
  "statistics": {
      "ファイル名": XX.mp3,
      "チェック日時": 2022-07-14 20:55:23,
      "ファイルフォーマット": "ファイルの読み込みに失敗しました"
    }
}
```
