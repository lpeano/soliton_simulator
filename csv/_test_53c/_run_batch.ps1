# TEST MOD 5.3c — UN BATCH = i 3 bracci per UN seed (esecuzione 3-a-3, Luca lavora nel frattempo).
# Uso: powershell -File csv/_test_53c/_run_batch.ps1 -seed 1   (poi -seed 2, -seed 3)
# Switch base IDENTICI al pilota 5.3a pulito + --verlet + --deparam-orologio (attiva _phc). --db-cleanup = fresh.
param([int]$seed = 1)
$ErrorActionPreference = "Continue"
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))  # root del repo
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
