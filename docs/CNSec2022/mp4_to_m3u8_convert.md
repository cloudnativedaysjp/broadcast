## ffmpeg を用いて簡易的に変換する（ABR非対応）

問題のあったアーカイブを録画から復旧する時や、"変換中動画" の作成など、最低限の設定で素早く変換する時用

### 環境

- ffmpeg (mac 版で動作確認済み）

### 変換コマンド

カレントディレクトリにある video.mp4 から playlist.m3u8 ファイルと、video%3d.ts というファイル群を作成する。 
```bash
ffmpeg -i video.mp4 -c:v copy -c:a copy -f hls -hls_time 9 -hls_playlist_type vod -hls_segment_filename "video%3d.ts" playlist.m3u8
```

## 格納先

s3://dreamkast-ivs-stream-archive-prd/mediapackage/cnsec2022/talks/ に `{talk_id}/{適当な2桁数字(下で使う)}` ディレクトリを掘って、そこに m3u8 と .ts ファイルを全部格納する 

https://s3.console.aws.amazon.com/s3/buckets/dreamkast-ivs-stream-archive-prd?prefix=mediapackage/cnsec2022/talks/&region=us-east-1 

## dk 管理画面で video_id の指定
https://event.cloudnativedays.jp/cnsec2022/admin/talks の talk_id を指定して保存

`https://d3pun3ptcv21q4.cloudfront.net/medialive/cnsec2022/talks/{talk_id}/{上で指定した適当な2桁数字}/playlist.m3u8`
