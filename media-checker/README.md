## media checker
指定した動画の解像度とアスペクト比を判定します。  
また、Flagが設定されている場合に動画長と動画容量を判定します。  

デフォルトの判定基準は、解像度: `FullHD`、アスペクト比: `16:9`、動画長: `35min - 45min`、動画容量: `< 1000MiB`。  
判定基準と違う場合に`NG`と判定されます。

### 使い方
```
python3 media_checker.py <動画データが格納されているdirectory名 または 動画ファイル名>
```

判定基準を変える場合は、以下の設定を変更します。
```bash
# Default criterion
# Target ratio
target_ratio = require_resolutions[2]["ratio"]
horizontal_criteria_ratio = 16
vertical_criteria_ratio = 9

# Target duration(min)
duration_upper_limit = 45
duration_lower_limit = 35
duration_flag = True

# Target file size(MiB)
size_upper_limit = 1000
size_flag = False
```

| Item | Description |
| :--  | :--  |
| target_ratio | `require_resolutions[X]["ratio"]` の `X`で判定する解像度を指定<br/> 0: SD, 1: HD, 2: FullHD, 3:  WQHD, 4: 4K|
| vertical_criteria_ratio | アスペクト比(横) |
| horizontal_criteria_ratio | アスペクト比(縦) |
| duration_upper_limit | 動画長の上限値(分) ※デフォルト45分 |
| duration_lower_limit | 動画長の下限値(分) ※デフォルト35分 |
| duration_flag | True(デフォルト)/False (Trueの場合に出力結果に動画長の判定結果を含める) |
| size_upper_limit | 動画の容量上限値 ※デフォルト1000MiB |
| size_flag | True/False(デフォルト) (Trueの場合に出力結果に動画容量の判定結果を含める) |

### 出力例
```bash
# duration_flag: False, size_flag: False
$ python3 media_checker.py media | jq
[
  {
    "file_name": "XX",
    "resolution_status": "NG",
    "resolution_type": "WQHD",
    "aspect_status": "OK",
    "aspect_ratio": "16:9"
  },
  {
    "file_name": "YY",
    "resolution_status": "OK",
    "resolution_type": "FullHD",
    "aspect_status": "OK",
    "aspect_ratio": "16:9"
  },
  {
    "file_name": "ZZ",
    "resolution_status": "NG",
    "resolution_type": "NON STANDARD",
    "aspect_status": "NG",
    "aspect_ratio": "1728 x 1080"
  }
]

# duration_flag: True, size_flag: True
[
  {
    "file_name": "XX",
    "resolution_status": "NG",
    "resolution_type": "WQHD",
    "aspect_status": "OK",
    "aspect_ratio": "16:9",
    "duration_status": "OK",
    "duration_description": "Appropriate media duration.",
    "size_status": "OK",
    "size_description": "Appropriate media size."
  }
]
```

| Item | Description |
| :--  | :--  |
| file_name | チェック対象の動画ファイル名 |
| resolution_status | OK/NG（デフォルトの判定基準と合致するか）|
| resolution_type" | SD/HD/FullHD/WQHD/4K（合致しない場合は`NON STANDARD`）|
| aspect_status | OK/NG（デフォルトの判定基準と合致するか）|
| aspect_ratio | 判定アスペクト比（合致しない場合は動画の縦横長）|
| duration_status | OK/NG（動画長が上限下限に収まっているか）|
| duration_description | 下限を下回る場合: The media duration is shorter than {下限値} minutes. <br>上限下限に収まっている場合: Appropriate media duration. <br>上限を超えている場合: The media duration is longer than {上限値} minutes. |
| size_status | OK/NG（動画容量が上限値を超えていないか) |
| size_description | 動画容量が規定値以内: Appropriate media size. <br>動画容量が規定値を超過している場合: The media size exceeds {上限値} MiB.|

### 要件
- ffmpeg
- Python3

検証時は
```bash
$ python3 --version
Python 3.8.10

$ ffmpeg -version
ffmpeg version 4.2.4-1ubuntu0.1 Copyright (c) 2000-2020 the FFmpeg developers
built with gcc 9 (Ubuntu 9.3.0-10ubuntu2)
```
