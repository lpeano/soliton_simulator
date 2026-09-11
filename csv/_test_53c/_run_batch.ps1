# TEST MOD 5.3c — UN BATCH = i 3 bracci per UN seed (esecuzione 3-a-3, Luca lavora nel frattempo).
# Uso: powershell -File csv/_test_53c/_run_batch.ps1 -seed 1   (poi -seed 2, -seed 3)
# Switch base IDENTICI al pilota 5.3a pulito + --verlet + --deparam-orologio (attiva _phc). --db-cleanup = fresh.
param([int]$seed = 1)
$ErrorActionPreference = "Continue"
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))  # root del repo

# GATE-CACHE GUARD (Luca 2026-09-11): cache ancorata al git BLOB di soliton_simulator.py (byte attuali,
# cattura anche modifiche NON committate). Cache-hit (blob invariato + PASS) -> parti istantaneo.
# Cache-miss/stale -> rigira il gate UNA volta (_gate.ps1, timbra la cache); se FAIL -> STOP. NON salta i
# gate, li CACHA: qualsiasi modifica al .py cambia il blob -> cache invalida -> ri-verifica.
$blobCur = (git hash-object soliton_simulator.py).Trim()
$cacheOk = $false
if (Test-Path "csv/_test_53c/gate_cache.json") {
  $c = Get-Content "csv/_test_53c/gate_cache.json" -Raw | ConvertFrom-Json
  if ($c.blob -eq $blobCur -and $c.gate_esito -eq "PASS") { $cacheOk = $true }
}
if ($cacheOk) {
  Write-Output "GATE CACHATI PASS (blob $($blobCur.Substring(0,12))... invariato) -> campagna sbloccata (istantaneo)."
} else {
  Write-Output "GATE CACHE MISS/STALE (blob $($blobCur.Substring(0,12))...) -> ri-verifico i gate UNA volta..."
  powershell -ExecutionPolicy Bypass -File csv/_test_53c/_gate.ps1
  if ($LASTEXITCODE -ne 0) { Write-Error "GATE FALLITO -> campagna BLOCCATA (non lancio i bracci)."; exit 2 }
}

$OUT = "csv/_test_53c"
$BASE = @("--batch","--nmasse","3","--sep","8","--passi","800","--ogni","100",
          "--campo-spinoriale","--spinore-vivo","--spinore-corretto","--chi-core",
          "--calore-scal","--deparam-orologio","--verlet")
$bracci = [ordered]@{
  "b1_base"        = @()
  "b2_orolseg"     = @("--orologio-segno")
  "b3_orolseg_cs"  = @("--orologio-segno","--cs-dinamico")
}
Write-Output "###### BATCH seed=$seed : b1_base, b2_orolseg, b3_orolseg_cs ######"
foreach ($nome in $bracci.Keys) {
  $tag = "${nome}_s${seed}"
  $diag = "$OUT/$tag.csv"; $cond = "$OUT/${tag}_cond.csv"; $db = "$OUT/$tag.pkl"
  $args = $BASE + $bracci[$nome] + @("--seed","$seed","--diaglog",$diag,"--csv",$cond,"--sync-db",$db,"--db-ogni","200","--db-cleanup")
  Write-Output "=== RUN $tag ==="
  Write-Output ("python soliton_simulator.py " + ($args -join " "))
  python soliton_simulator.py @args
  Write-Output "=== FINE $tag (exit $LASTEXITCODE) ==="
}
Write-Output "###### BATCH seed=$seed COMPLETATO ######"
