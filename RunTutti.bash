#!/usr/bin/env bash
# =============================================================================
#  run_tutti.bash - esegue TUTTI i test batch e i video a 10000 passi in parallelo.
#  Linux / Mac.  Uso:  bash run_tutti.bash
#
#  Canonico: soliton_simulator.py (determ + forma pura + calcio vettoriale di default).
#  Il diaglog ora scrive AUTOMATICAMENTE anche le colonne del test gauge emergente:
#    centro_N/coer/cosphi  (struttura collettiva al centro: cosphi<0 = antifase = pozzo/valle)
#    guscio_N/coer/cosphi/circ  (buccia attorno alle masse; circ = olonomia = firma gauge)
#  I test: 2 e 3 masse, confronto calcio vett/scalare, confronto d/d0.
# =============================================================================

set -u
SIM=soliton_simulator.py
PASSI=10000
FRAMES=10000
SEP=8
mkdir -p out_test out_video log

echo "=== Avvio di tutti i test in parallelo (10000 passi). Log in ./log/ ==="
echo "    CPU disponibili: $(nproc 2>/dev/null || echo '?')  -- ogni processo usa ~1 core"
echo ""

batch () {  # $1=nome  $2...=flag extra
  local nome=$1; shift
  echo "[batch] avvio $nome"
  python3 "$SIM" --batch --nmasse "$NM" --sep "$SEP" --passi "$PASSI" --ogni 5 "$@" \
    --csv "out_test/cond_${nome}.csv" --diaglog "out_test/diag_${nome}.csv" \
    > "log/${nome}.log" 2>&1 &
}
video () {  # $1=nome  $2...=flag extra
  local nome=$1; shift
  echo "[video] avvio $nome"
  python3 "$SIM" --test "N-MASSE" --nmasse "$NM" --sep "$SEP" --giri 0 --ppf 1 \
    --frames "$FRAMES" --fps 24 "$@" --out "out_video/${nome}.mp4" \
    > "log/${nome}_video.log" 2>&1 &
}

# ============ 2 MASSE ============
NM=2
batch  "2m_default"                  # d + calcio vettoriale (default)
batch  "2m_scalare"  --calore-scal   # calcio scalare (confronto A/B)
batch  "2m_d0"       --tau-d0        # forma d0
video  "2m_default"
video  "2m_d0"       --tau-d0

# ============ 3 MASSE ============
NM=3
batch  "3m_default"                  # d + calcio vettoriale (default)
batch  "3m_scalare"  --calore-scal   # calcio scalare (A/B - test frustrazione)
batch  "3m_d0"       --tau-d0        # forma d0
video  "3m_default"
video  "3m_d0"       --tau-d0

echo ""
echo "=== Tutti i processi lanciati in parallelo. Attendo il completamento... ==="
echo "    (segui i log:  tail -f log/*.log )"
wait
echo ""
echo "=== FINITO. Risultati in:  out_test/ (CSV)  out_video/ (mp4)  log/ (log) ==="