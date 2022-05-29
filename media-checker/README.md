## media checker
指定した動画の解像度とアスペクト比を判定します。  
デフォルトの判定基準は、解像度: `FullHD`、アスペクト比: `16:9`。  
判定基準と違う場合に`NG`と判定されます。

### 使い方
```
python3 media_checker.py <動画データが格納されているdirectory名 または 動画ファイル名>
```

判定基準を変える場合は、以下の設定を変更します。
```
target_ratio = require_resolutions[2]["ratio"]
vertical_criteria_ratio = 16
horizontal_criteria_ratio = 9
```

| Item | Description |
| :--  | :--  |
| target_ratio | `require_resolutions[X]["ratio"]` の `X`で判定する解像度を指定<br/> 0: SD, 1: HD, 2: FullHD, 3:  WQHD, 4: 4K|
| vertical_criteria_ratio | アスペクト比(横) |
| horizontal_criteria_ratio | アスペクト比(縦) |

### 出力例
```
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
```

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
