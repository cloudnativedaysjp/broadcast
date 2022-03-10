# IPアドレス・ホスト一覧

## 配信PC
ホスト名 | IPアドレス | 機材 | 備考
-- | -- | -- | --
broadcast-obs-A | 192.168.199.11 | TUF Gaming | NDIセグメント（内蔵 NIC）
broadcast-obs-A | DHCP | TUF Gaming | グローバルセグメント（USB NIC）
broadcast-obs-B | 192.168.199.12 | TUF Gaming | NDIセグメント（内蔵 NIC）
broadcast-obs-B | DHCP | TUF Gaming | グローバルセグメント（USB NIC）
broadcast-obs-C | 192.168.199.13 | TUF Gaming | NDIセグメント（内蔵 NIC）
broadcast-obs-C | DHCP | TUF Gaming | グローバルセグメント（USB NIC）
atem-mini-03 | 192.168.199.23 | ATEM Mini | NDIセグメント
atem-mini-04 | 192.168.199.24 | ATEM Mini | NDIセグメント

## リモート登壇用PC
### リモート3
ホスト名 | IPアドレス | 機材 | 備考
-- | -- | -- | --
remote-obs-03 | 192.168.199.31 | TUF Gaming | NDIセグメント（内蔵 NIC）
remote-zoom-03 | 192.168.199.32 | Dynabook | NDIセグメント（内蔵 NIC）
remote-l2sw-03 | 192.168.199.39 | Netgear SW | 

### リモート4
ホスト名 | IPアドレス | 機材 | 備考
-- | -- | -- | --
remote-obs-04 | 192.168.199.41 | TUF Gaming | NDIセグメント（内蔵 NIC）
remote-zoom-04 | 192.168.199.42 | Dynabook | NDIセグメント（内蔵 NIC）
remote-l2sw-04 | 192.168.199.49 | Netgear SW | 

### モニタリング
ホスト名 | IPアドレス | 機材 | 備考
-- | -- | -- | --
broadcast-monitoring-linux | DHCP | Hyper-V | グローバルセグメント（eth0）
broadcast-monitoring-linux | 192.168.199.211 | Hyper-V | NDIセグメント（eth1）

## ネットワーク機器
ホスト名 | IPアドレス | 機材 | 備考
-- | -- | -- | --
| - | 192.168.199.253 | Cisco 2960S
| - | DHCP | Cisco Meraki Go
