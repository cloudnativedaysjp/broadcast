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

