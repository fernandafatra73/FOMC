# Membuat "FOMC Dashboard.exe" dari fomc-dashboard.html.
# Pemakaian:  powershell -ExecutionPolicy Bypass -File launcher\build.ps1 [-Out <path exe>]
# Default output: Desktop pengguna. Butuh Python (untuk ikon) dan .NET Framework 4 (bawaan Windows).
param(
    [string]$Out = (Join-Path ([Environment]::GetFolderPath('Desktop')) 'FOMC Dashboard.exe')
)
$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$html = Join-Path $root 'fomc-dashboard.html'
$csc  = Join-Path $env:WINDIR 'Microsoft.NET\Framework64\v4.0.30319\csc.exe'
if (-not (Test-Path $csc)) { $csc = Join-Path $env:WINDIR 'Microsoft.NET\Framework\v4.0.30319\csc.exe' }
if (-not (Test-Path $csc)) { throw 'csc.exe (.NET Framework 4) tidak ditemukan.' }

$build = Join-Path $env:TEMP 'fomc-launcher-build'
New-Item -ItemType Directory -Force $build | Out-Null
$ico = Join-Path $build 'fomc.ico'

python (Join-Path $here 'make_icon.py') $ico
if ($LASTEXITCODE -ne 0) { throw 'Gagal membuat ikon.' }

& $csc /nologo /target:winexe /optimize+ "/out:$Out" "/win32icon:$ico" `
    "/resource:$html,fomc-dashboard.html" /reference:System.Windows.Forms.dll `
    (Join-Path $here 'Program.cs')
if ($LASTEXITCODE -ne 0) { throw 'Kompilasi gagal.' }

Get-Item $Out | Select-Object FullName, Length, LastWriteTime
