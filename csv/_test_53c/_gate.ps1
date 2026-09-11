# GATE + CACHE ancorata al git BLOB di soliton_simulator.py (byte ATTUALI: cattura anche modifiche NON
# committate, a differenza del commit hash). Stesso principio del DB di stato (_versione_codice/git hash-object).
# Verifica il PRESIDIO VIVO (purezza diaglog byte-identica + metrica non-tautologica + baseline ~0) sul codice
# attuale; su PASS timbra gate_cache.json col blob. Cache-hit nel launcher = gate istantanei. Cache-miss = qui.
# NB: i sigilli firma (OFF byte-id, riduzione-al-limite, norma) sono ANALITICI (s_k=1.0 -> exp identico) e
# verificati al sigillo 77c83e5; il gate vivo che puo' regredire con una modifica al diaglog e' il presidio.
$ErrorActionPreference = "Continue"
Set-Location (Split-Path -Parent (Split-Path -Parent $PSScriptRoot))  # root del repo
$blob = (git hash-object soliton_simulator.py).Trim()
$commit = (git rev-parse HEAD).Trim()
Write-Output "=== GATE (blob $($blob.Substring(0,12))...): _check_presidio.py ==="
python csv/_seal_53c/_check_presidio.py
if ($LASTEXITCODE -eq 0) {
  $cache = [ordered]@{
    blob        = $blob
    gate_esito  = "PASS"
    presidi     = [ordered]@{ diaglog_byte_id = $true; metrica_non_tautologica = $true; baseline_zero = $true }
    sigilli     = [ordered]@{ off_byte_id = $true; riduzione_limite = $true; norma = $true; stabilita = $true;
                              nota = "analitici (s_k=1.0 -> exp identico) + verificati al sigillo 77c83e5" }
    data        = (Get-Date -Format o)
    commit      = $commit
    config      = "batch nmasse3 sep8 800p campo-spinoriale spinore-vivo spinore-corretto chi-core calore-scal deparam-orologio verlet"
  }
  $cache | ConvertTo-Json -Depth 4 | Set-Content csv/_test_53c/gate_cache.json
  Write-Output "GATE PASS -> gate_cache.json timbrato (blob $($blob.Substring(0,12))...). Campagna SBLOCCATA."
  exit 0
} else {
  if (Test-Path csv/_test_53c/gate_cache.json) { Remove-Item csv/_test_53c/gate_cache.json }
  Write-Output "GATE FALLITO -> cache rimossa. Campagna BLOCCATA (correggi e ri-esegui il gate)."
  exit 1
}
