Param($Args1,$Args2)


## IP Setting
echo ">>> Start ip address setting"
New-NetIPAddress -InterfaceIndex ${Args2} -AddressFamily IPv4 -IPAddress ${Args1} -PrefixLength 24 -DefaultGateway 192.168.199.254

## Disable firewall
echo ">>> Disable firewall"
Get-NetFirewallProfile | Set-NetFirewallProfile -Enabled false

## Cortana Uninstall
echo ">>> Uninstall Cortana"
Get-AppxPackage -allusers Microsoft.549981C3F5F10 | Remove-AppxPackage

## Setup Chocolatey
echo ">>> setup chocolatey"
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# obs
echo ">>> Install OBS Studio"
choco install obs-studio -y

# install nextcloud-client
echo ">>> install nextcloud-client"
choco install nextcloud-client -y

# install vlc-media-player
echo ">>> install vlc-media-player"
choco install vlc

## Windows Exporter
echo ">>> Setup windows exporter"
Invoke-RestMethod -ContentType "application/octet-stream" -Uri https://github.com/prometheus-community/windows_exporter/releases/download/v0.16.0/windows_exporter-0.16.0-386.exe -OutFile "~\Downloads\windows-exporter.exe"

Copy-Item "~\Downloads\windows-exporter.exe" "~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" -Recurse

# obs-ndi
echo ">>> Start downloading obs-ndi in zip format"
Invoke-RestMethod -ContentType "application/octet-stream" -Uri https://github.com/Palakis/obs-ndi/releases/download/4.9.1/obs-ndi-4.9.0-Windows.zip -OutFile "~\Downloads\obs-ndi-4.9.0-Windows.zip"
echo ">>> Unarchive a  zip file of obs-ndi"
Unblock-File -Path "~\Downloads\obs-ndi-4.9.0-Windows.zip"
Expand-Archive -Path "~\Downloads\obs-ndi-4.9.0-Windows.zip" -DestinationPath "~\Downloads\obs-ndi"
echo ">>> Copy plugins to existing obs directory"
Copy-Item ~\Downloads\obs-ndi\data\obs-plugins\obs-ndi 'C:\Program Files\obs-studio\data\obs-plugins' -Recurse
Copy-Item ~\Downloads\obs-ndi\obs-plugins\64bit\* 'C:\Program Files\obs-studio\obs-plugins\64bit' -Recurse

# NDI-Tools
echo ">>> Start downloading NDI-Tools in exe format"
Invoke-RestMethod -ContentType "application/octet-stream" -Uri https://downloads.ndi.tv/Tools/NDI%205%20Tools.exe -OutFile "~\Downloads\NDI-Tools.exe"
~\Downloads\NDI-Tools.exe
