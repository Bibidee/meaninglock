$ErrorActionPreference = 'Stop'
$contract = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\contracts\meaning_lock.py'))
$candidates = Get-ChildItem (Split-Path $contract) -Filter '*.py' -File
if ($candidates.Count -ne 1 -or $candidates[0].FullName -ne $contract) { throw 'contracts must contain only meaning_lock.py' }
if (-not (Select-String -Path $contract -Pattern 'class MeaningLock\(gl.Contract\)' -Quiet)) { throw 'contract class missing' }
if ((Select-String -Path $contract -Pattern 'emit_transfer' | Measure-Object).Count -ne 1) { throw 'exactly one transfer emission expected' }
Write-Output 'release structural checks passed'
