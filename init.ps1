$ErrorActionPreference = "Stop"

$Root = $PSScriptRoot
$Venv = Join-Path $Root ".venv"
$Req = Join-Path $Root "requirements.txt"
$BinDir = Join-Path $env:LOCALAPPDATA "CoreUtils\bin"
$Launcher = Join-Path $BinDir "devdrop.cmd"

if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw "Python 3 is required." }
if (-not (Test-Path (Join-Path $Venv "Scripts\python.exe"))) {
    python -m venv $Venv
}

$VenvPython = Join-Path $Venv "Scripts\python.exe"
& $VenvPython -m pip install -r $Req

New-Item -ItemType Directory -Force -Path $BinDir | Out-Null
@"
@echo off
cd /d "$Root"
"$VenvPython" main.py %*
"@ | Set-Content -Path $Launcher -Encoding ASCII

Write-Host "DevDrop initialized."
Write-Host "Launcher installed at $Launcher"
