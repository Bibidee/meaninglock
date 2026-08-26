$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $python) { $python = (Get-Command py -ErrorAction SilentlyContinue).Source }
$lint = (Get-Command genvm-lint -ErrorAction SilentlyContinue).Source
if (-not $lint) { $lint = (Get-Command genvm-linter -ErrorAction SilentlyContinue).Source }
if (-not $python -or -not $lint) { throw 'Required python and genvm-lint executables were not found on PATH.' }
$env:PYTHONUTF8 = '1'
$env:Path = (Split-Path $lint) + ';' + $env:Path
Push-Location $root
try {
  & $lint check contracts/meaning_lock.py
  & $lint validate contracts/meaning_lock.py
  & $lint schema contracts/meaning_lock.py --output evidence/meaning_lock.schema.json
  & $lint typecheck contracts/meaning_lock.py
  & $python -m pytest tests/direct tests/integration -v
  & (Join-Path $root 'scripts/release_check.ps1')
} finally { Pop-Location }
