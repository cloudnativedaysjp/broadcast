Setup OBS, Desktop environment and NVIDIA Driver for Ubuntu 20.04
=================================================================

````````oi
```
sudo add-apt-repository -y ppa:obsproject/obs-studio
sudo apt-get update
sudo apt-get install -y lightdm
# ↑lightdmを選択。 インストール自動化するときはここの選択操作を自動化どうやるか要調査

sudo apt-get install -y ubuntu-drivers-common  nvidia-driver-460 ocl-icd-libopencl1 opencl-headers clinfo obs-studio ffmpeg ubuntu-desktop x11vnc net-tools

#dreamkast のところはVNC接続時に使うパスワード。自動化の時は環境変数で渡した方がいいかも
sudo x11vnc -storepasswd dreamkast /etc/.vncpasswd  

sudo sh -c "cat <<EOF > /etc/systemd/system/x11vnc.service
[Unit]
Description=x11vnc (Remote access)
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/x11vnc -auth guess -display :0 -rfbauth /etc/.vncpasswd -rfbport 5900 -forever -loop -noxdamage -repeat -shared
ExecStop=/bin/kill -TERM $MAINPID
ExecReload=/bin/kill -HUP $MAINPID
KillMode=control-group
Restart=on-failure

[Install]
WantedBy=graphical.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable x11vnc
sudo systemctl start x11vnc

sudo reboot

#利用するユーザーのパスワードを設定
sudo passwd ubuntu 
```
