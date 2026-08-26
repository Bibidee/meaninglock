$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$python = 'C:\Users\ojiku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$lint = 'C:\Users\ojiku\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Scripts\genvm-lint.exe'
$env:PYTHONUTF8 = '1'
$env:Path = (Split-Path $lint) + ';' + $env:Path
Push-Location $root
try {
  & $lint lint contracts/meaning_lock.py
  & $lint validate contracts/meaning_lock.py
  & $lint schema contracts/meaning_lock.py --output evidence/meaning_lock.schema.json
  & $lint typecheck contracts/meaning_lock.py
  & $python -m pytest tests/direct tests/integration -v
  & (Join-Path $root 'scripts/release_check.ps1')
} finally { Pop-Location }
