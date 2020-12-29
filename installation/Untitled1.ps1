if( -not ([bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")))
{
Write-Host "Pls run as admin"
Read-Host
exit
}

New-Item -Path "$env:APPDATA\PEKO\Log" -ItemType Directory
New-Item -Path "$env:APPDATA\PEKO\Data" -ItemType Directory
New-Item -Path "$env:APPDATA\PEKO\bin" -ItemType Directory
New-Item -Path "$env:APPDATA\PEKO\Front" -ItemType Directory

Copy-Item

$pass = Read-Host("give password")
setx test ([convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pass)))

Set-Itemproperty -path 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' -Name 'PEKO' -value "$env:APPDATA\PEKO\bin\PekoInstallations.exe"

Import-Module IISAdministration
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-DefaultDocument" -All

$sitefolder = "$env:APPDATA\PEKO\Front"
$sitename = "PEKOINSTALLATIONS"

# make IIS website
New-IISSite -Name $sitename -PhysicalPath $sitefolder -BindingInformation ("*:80:" + $sitename)

# start pool in case it did not
Start-WebAppPool -Name "DefaultAppPool"
Remove-IISSite -Name "Peko"
