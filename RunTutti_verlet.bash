#!/usr/bin/env bash
# Variante Velocity-Verlet del run generale Unix.
set -u
SIM=soliton_simulator.py
PASSI=10000
SEP=8
mkdir -p out_test out_video log
batch () {
  local nome=$1; shift
  python3 "$SIM" --batch --nmasse "$NM" --sep "$SEP" --passi "$PASSI" --ogni 5 --verlet "$@" \
    --csv "out_test/cond_${nome}_verlet.csv" --diaglog "out_test/diag_${nome}_verlet.csv" \
    > "log/${nome}_verlet.log" 2>&1 &
}
video () {
  local nome=$1; shift
  python3 "$SIM" --test "N-MASSE" --nmasse "$NM" --sep "$SEP" --giri 0 --ppf 1 \
    --frames "$PASSI" --fps 24 --verlet "$@" --out "out_video/${nome}_verlet.mp4" \
    > "log/${nome}_video_verlet.log" 2>&1 &
}
NM=2
batch 2m_default
batch 2m_scalare --calore-scal
batch 2m_d0 --tau-d0
video 2m_default
video 2m_d0 --tau-d0
NM=3
batch 3m_default
batch 3m_scalare --calore-scal
batch 3m_d0 --tau-d0
video 3m_default
video 3m_d0 --tau-d0
wait
echo "=== Run Velocity-Verlet completato ==="
