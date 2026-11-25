# Збирає звіт і слайди: .\build.ps1   (з папки проєкту, у PowerShell)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot

# Quarto: з PATH або з D:\tools\quarto
$quarto = (Get-Command quarto -ErrorAction SilentlyContinue).Source
if (-not $quarto) { $quarto = 'D:\tools\quarto\bin\quarto.exe' }
if (-not (Test-Path $quarto)) { throw 'Quarto не знайдено. Встановіть з https://quarto.org/docs/get-started/' }

# Python, у який встановлено requirements.txt
if (-not $env:QUARTO_PYTHON) {
    $venv = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (Test-Path $venv) { $env:QUARTO_PYTHON = $venv }
    else { $env:QUARTO_PYTHON = (& python -c "import sys; print(sys.executable)").Trim() }
}

# тимчасові файли Quarto в папці проєкту (обхід помилки "could not be encrypted" на деяких Windows)
$tmp = Join-Path $PSScriptRoot '.tmp'
New-Item -ItemType Directory -Force "$tmp\local" | Out-Null
$env:TMP = $tmp; $env:TEMP = $tmp; $env:LOCALAPPDATA = "$tmp\local"

& $quarto render
if ($LASTEXITCODE -ne 0) { throw 'Збирання не вдалося' }
Start-Process (Join-Path $PSScriptRoot 'report.html')
Write-Host 'Готово: report.html і slides.html оновлено.'
