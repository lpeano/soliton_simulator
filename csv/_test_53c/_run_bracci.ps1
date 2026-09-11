# TEST MOD 5.3c (--orologio-segno) — 3 BRACCI x seed, sequenziale (OOM: 1 per volta), resumibile (--sync-db).
# Switch base IDENTICI al pilota 5.3a pulito (on_scal_s1.csv), TRANNE le firme. + --deparam-orologio (attiva _phc).
#   B1 BASELINE : base
#   B2 5.3c     : base --orologio-segno
#   B3 5.3c+cs  : base --orologio-segno --cs-dinamico
# Ordine: seed 1 tutti i bracci, poi seed 2, poi seed 3 (primo sguardo dopo seed 1).
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))  # root del repo
$OUT = "csv/_test_53c"
$BASE = @("--batch","--nmasse","3","--sep","8","--passi","800","--ogni","100",
          "--campo-spinoriale","--spinore-vivo","--spinore-corretto","--chi-core",
          "--calore-scal","--deparam-orologio","--verlet")
$bracci = @{
  "b1_base"        = @()
  "b2_orolseg"     = @("--orologio-segno")
  "b3_orolseg_cs"  = @("--orologio-segno","--cs-dinamico")
}

# RI-CONFERMA 5.3a PULITO (presidio Luca #2): --tempo-segno seed 1 su fisica pulita (diaglog fixato).
# Da confrontare col baseline b1_base_s1 -> il verdetto NO-GO regge senza contaminazione?
$tag5 = "r53a_tsegno_s1"
$args5 = $BASE + @("--tempo-segno","--seed","1","--diaglog","$OUT/$tag5.csv","--csv","$OUT/${tag5}_cond.csv","--sync-db","$OUT/$tag5.pkl","--db-ogni","200")
Write-Output "=== RUN $tag5 (ri-conferma 5.3a pulito) ==="
Write-Output ("python soliton_simulator.py " + ($args5 -join " "))
python soliton_simulator.py @args5
Write-Output "=== FINE $tag5 (exit $LASTEXITCODE) ==="

foreach ($seed in 1,2,3) {
  foreach ($nome in "b1_base","b2_orolseg","b3_orolseg_cs") {
    $tag = "${nome}_s${seed}"
    $diag = "$OUT/$tag.csv"
    $cond = "$OUT/${tag}_cond.csv"
    $db   = "$OUT/$tag.pkl"
    $args = $BASE + $bracci[$nome] + @("--seed","$seed","--diaglog",$diag,"--csv",$cond,"--sync-db",$db,"--db-ogni","200")
    Write-Output "=== RUN $tag ==="
    Write-Output ("python soliton_simulator.py " + ($args -join " "))
    python soliton_simulator.py @args
    Write-Output "=== FINE $tag (exit $LASTEXITCODE) ==="
  }
}
Write-Output "TUTTI I BRACCI COMPLETATI"
