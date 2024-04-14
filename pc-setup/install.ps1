$ProgressPreference = 'SilentlyContinue'

cd ~/Downloads
echo "Downloading installer.."
echo "Start downloading winget-cli"
Invoke-WebRequest -UseBasicParsing -Uri https://github.com/microsoft/winget-cli/releases/download/v1.6.3133/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle -OutFile .\Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle
echo "Start downloading VCLibs"
Invoke-WebRequest -UseBasicParsing -Uri https://aka.ms/Microsoft.VCLibs.x64.14.00.Desktop.appx -OutFile Microsoft.VCLibs.x64.14.00.Desktop.appx
echo "Start downloading companion-module-roland-vr6hd"
Invoke-WebRequest -UseBasicParsing -Uri https://github.com/cloudnativedaysjp/companion-module-roland-vr6hd/archive/refs/heads/main.zip -OutFile companion-module-roland-vr6hd.zip
echo "Start downloading companion"
Invoke-WebRequest -UseBasicParsing -Uri https://uploader.cloudnativedays.jp/s/RpyYYc4gK8bm3DD/download/companion-win64-3.0.1+6068-stable-a05a9c89.exe -OutFile companion-win64-3.0.1+6068-stable-a05a9c89.exe
echo "Start downloading cndctl"
Invoke-WebRequest -UseBasicParsing -Uri https://github.com/cloudnativedaysjp/cndctl/archive/refs/heads/master.zip -OutFile ~/Downloads/cndctl.zip
$ProgressPreference = 'Continue'


echo "Enable remote desktop"
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name  "fDenyTSConnections" -Value "0"
Set-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" -Name "UserAuthentication" -Value 1

echo "Disable Windows Update"
Set-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "AUOptions" -Value "1"
Set-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU" -Name "NoAutoUpdate" -Value "1"

echo "Installing winget"
Add-AppxPackage Microsoft.VCLibs.x64.14.00.Desktop.appx
Add-AppxPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle

echo "Running winget"
winget install OBSProject.OBSStudio --accept-package-agreements --accept-source-agreements
winget install Nextcloud.NextcloudDesktop --accept-package-agreements --accept-source-agreements
winget install Python.Python.3.12 --accept-package-agreements --accept-source-agreements
winget install Git.Git --accept-package-agreements --accept-source-agreements
winget install Microsoft.VisualStudioCode
winget install tailscale.tailscale --accept-package-agreements --accept-source-agreements
winget install VideoLAN.VLC --accept-package-agreements --accept-source-agreements
winget install Elgato.StreamDeck --accept-package-agreements --accept-source-agreements
winget install OpenJS.NodeJS.LTS  --accept-package-agreements --accept-source-agreements
winget install Google.Chrome  --accept-package-agreements --accept-source-agreements

echo "Turning off firewalls"
netsh advfirewall set allprofiles state off

echo "Extract cndctl and companion modules"
Expand-Archive -Path ~/Downloads/cndctl.zip -DestinationPath ~/Documents/
Expand-Archive -Path ~/Downloads\companion-module-roland-vr6hd.zip -DestinationPath ~/Documents/

echo "Installing companion"
~/Downloads/companion-win64-3.0.1+6068-stable-a05a9c89.exe /SILENT
