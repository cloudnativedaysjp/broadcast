# Windowsを構築する
## ネットワークに
DHCPで接続する。
接続インターフェイスは、USB NICを利用する。

## 自動構築PS1の流し込み


```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted
Invoke-RestMethod -ContentType "application/octet-stream" -Uri https://raw.githubusercontent.com/cloudnativedaysjp/dreamkast-broadcast/main/sandbox/Install-script.ps1 -OutFile "~\Downloads\Install-script.ps1"
powershell.exe ~\Downloads\Install-script.ps1 192.168.199.${YOUR_IP} ${NIC_INDEX} ${HOSTNAME}
```

`${NIC_INDEX}`は`Get-NetAdapter`コマンド結果の`ifIndex`をもとに決める
```
PS C:\Windows\system32> Get-NetAdapter

Name                     InterfaceDescription                    ifIndex Status       MacAddress             LinkSpeed
----                     --------------------                    ------- ------       ----------             ---------
イーサネット 2            Microsoft Hyper-V Network Adapter #2         10 Up           00-15-5D-14-02-1D        10 Gbps
イーサネット              Microsoft Hyper-V Network Adapter             3 Up           00-15-5D-14-02-1C        10 Gbps
```

## シンボリックリンクの作成
```powershell
Remove-Item -Recurse ~\AppData\Roaming\obs-studio
New-Item -type SymbolicLink ~\Videos\o11y2022 -Value ~\Nextcloud\Broadcast\o11y2022\Sync\Media
New-Item -type SymbolicLink ~\AppData\Roaming\obs-studio -Value ~\Nextcloud\Broadcast\o11y2022\Sync\OBS-Settings\${TRACK_DIR}
```

## 再起動

## NextCloudのセットアップ
- ログイン
- フォルダの指定
