Param($Args1,$Args2,$Args3)

echo "User is ${Args1}"


## IP Setting
New-NetIPAddress -InterfaceAlias "イーサネット" -AddressFamily IPv4 -IPAddress ${Args2} -PrefixLength 24 -DefaultGateway ${Args3}

## Cortana Uninstall
Get-AppxPackage -allusers Microsoft.549981C3F5F10 | Remove-AppxPackage

## Windows Exporter
Invoke-WebRequest https://github.com/prometheus-community/windows_exporter/releases/download/v0.16.0/windows_exporter-0.16.0-386.exe -UseBasicParsing -OutFile "C:\Users\${Args1}\Downloads\windows-exporter.exe"

Copy-Item "C:\Users\${Args1}\Downloads\windows-exporter.exe" "C:\Users\ry\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" -Recurse

# obs
echo ">>> Start downloading OBS Studio in zip format"
Invoke-WebRequest https://cdn-fastly.obsproject.com/downloads/OBS-Studio-27.1.3-Full-x64.zip -UseBasicParsing -OutFile "C:\Users\${Args1}\Downloads\OBS-Studio-27.1.3-Full-x64.zip"
echo ">>> Unarchive a  zip file of OBS Studio"
Unblock-File -Path "C:\Users\${Args1}\Downloads\OBS-Studio-27.1.3-Full-x64.zip"
Expand-Archive -Path "C:\Users\${Args1}\Downloads\OBS-Studio-27.1.3-Full-x64.zip" -DestinationPath "C:\Users\${Args1}\Downloads\obs-studio"
echo ">>> Copy Program files"
Copy-Item C:\Users\${Args1}\Downloads\obs-studio 'C:\Program Files\' -Recurse
## ショートカット作成
echo ">>> Create shortcut"
$WsShell = New-Object -ComObject WScript.Shell
$Shortcut = $WsShell.CreateShortcut("C:\Users\${Args1}\Desktop\OBS Studio.lnk")
$Shortcut.TargetPath = 'C:\Program Files\obs-studio\bin\64bit\obs64.exe'
$Shortcut.WorkingDirectory = 'C:\Program Files\obs-studio\bin\64bit\'
$Shortcut.Save()


# obs-ndi
echo ">>> Start downloading obs-ndi in zip format"
Invoke-WebRequest https://github.com/Palakis/obs-ndi/releases/download/4.9.1/obs-ndi-4.9.0-Windows.zip -UseBasicParsing -OutFile "C:\Users\${Args1}\Downloads\obs-ndi-4.9.0-Windows.zip"
echo ">>> Unarchive a  zip file of obs-ndi"
Unblock-File -Path "C:\Users\${Args1}\Downloads\obs-ndi-4.9.0-Windows.zip"
Expand-Archive -Path "C:\Users\${Args1}\Downloads\obs-ndi-4.9.0-Windows.zip" -DestinationPath "C:\Users\${Args1}\Downloads\obs-ndi"
echo ">>> Copy plugins to existing obs directory"
Copy-Item C:\Users\${Args1}\Downloads\obs-ndi\data\obs-plugins\obs-ndi 'C:\Program Files\obs-studio\data\obs-plugins' -Recurse
Copy-Item C:\Users\${Args1}\Downloads\obs-ndi\obs-plugins\64bit\* 'C:\Program Files\obs-studio\obs-plugins\64bit' -Recurse

# NDI-Tools
echo ">>> Start downloading NDI-Tools in exe format"
Invoke-WebRequest https://downloads.ndi.tv/Tools/NDI%205%20Tools.exe -UseBasicParsing -OutFile "C:\Users\${Args1}\Downloads\NDI-Tools.exe"
