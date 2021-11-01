AWS MediaConvertを使うスクリプト群
=================================

## Prerequisites

- Ruby実行環境 (2.7以降)
- AWS CLI v2

Rubyが入った環境で以下のコマンドを実行する
```
bundle install
```

また、AWS CLIでログインを済ませておく。
```
aws configure
```

## upload-and-convert.rb
提出された動画ファイルのファイル名と、セッション一覧のCSVを突合してS3にアップロード。その後、MediaConvertでHLS形式に変換をおこない、指定されたS3に保存するためのスクリプト。

例:
```
& ls -l
total 4796336
-rwxrwxrwx 1 jacopen jacopen 122331136 Oct 26 18:04 1A-1240-1300-Taichi_Nakashima.mp4
-rwxrwxrwx 1 jacopen jacopen 702200595 Oct 25 15:37 1A-1420-1500-MS.mp4
-rwxrwxrwx 1 jacopen jacopen 147237060 Oct 19 11:35 1B-1840-1900-Masaya_Tahara.mp4
-rwxrwxrwx 1 jacopen jacopen     80580 Oct 31 12:38 talks.csv
-rwxrwxrwx 1 jacopen jacopen     10990 Nov  1 23:27 upload-and-convert.rb
```
upload-and-convert.rbと同一のフォルダに提出動画を設置。提出動画にはtalkのIDが含まれていないため、Dreamkast側で取り扱いづらい。

talks.csvにはセッション情報が含まれているため、スクリプトは提出動画のファイル名からConference DayとTrack名、登壇時間をパースしCSVと突合する。その後、S3の `s3://dreamkast-ivs-stream-archive-prd/source/#{id}.mp4` にアップロードする。 

アップロード後、MediaConvertのAPIを叩いて変換を行う。 `s3://dreamkast-ivs-stream-archive-prd/source/#{id}.mp4` より動画を読み取り、 `s3://dreamkast-ivs-stream-archive-prd/medialive/cndt2021/talks/#{id}/` に変換完了したHLS動画を保存する。

実行するにはRubyでこのスクリプトを実行するだけでよい。

```
ruby upload-and-convert.rb
```

## convert.rb

WIP