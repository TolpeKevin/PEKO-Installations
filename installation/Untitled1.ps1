if( -not ([bool](([System.Security.Principal.WindowsIdentity]::GetCurrent()).groups -match "S-1-5-32-544")))
{
Write-Host "Pls run as admin"
Read-Host
exit
}


# make folders and copy files
New-Item -Path "$env:APPDATA\PEKO\Log" -ItemType Directory
New-Item -Path "$env:APPDATA\PEKO\Data" -ItemType Directory
New-Item -Path "$env:APPDATA\PEKO\bin" -ItemType Directory
New-Item -Path "$env:APPDATA\PEKO\Front" -ItemType Directory

Copy-Item -Path "$PSScriptRoot/Peko/front/*" -Destination "$env:APPDATA\PEKO\Front"
Copy-Item -Path "$PSScriptRoot/Peko/bin/*" -Destination "$env:APPDATA\PEKO\bin"
Copy-Item -Path "$PSScriptRoot/Peko/data/*" -Destination "$env:APPDATA\PEKO\Data"


# set pass as environment variable
$pass = Read-Host("give password")
setx test ([convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($pass)))

# set startup 
Set-Itemproperty -path 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run' -Name 'PEKO' -value "$env:APPDATA\PEKO\bin\PekoInstallations.exe"

# enable IIS
Enable-WindowsOptionalFeature -Online -FeatureName "IIS-DefaultDocument" -All

$sitefolder = "$env:APPDATA\PEKO\Front"
$sitename = "PEKOINSTALLATIONS"

# make IIS website
New-IISSite -Name $sitename -PhysicalPath $sitefolder -BindingInformation ("*:8080:")

