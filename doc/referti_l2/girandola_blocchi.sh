#!/bin/bash
# ### [M0329-F1] [M0329-M1] I BLOCCHI DELLA GIRANDOLA OLTRE QUELLI GIA' FATTI, UNO ALLA VOLTA (Luca 2026-11-22 10:32; la carta doc/TASK_HISTORY/2026-11-22_girandola_chi.md, sez. 7). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/girandola_blocchi.sh film t120 t120r28 t000     i film in E:\soliton_simulator\controllo\girandola_blocchi (fuori dal repo)
#   bash doc/referti_l2/girandola_blocchi.sh giro t120 t120r28 t000     le misure dei blocchi (i film gia' copiati in doc/referti_l2/film)
# I blocchi: da DA0 (t120, t120r28: 6000; t000: 2000) a passi di 2000, l'ultimo fino all'ultimo stato salvato quando la catena parte.
# Gia' fatto (il file di testo con la riga finale) = saltato: la catena si puo' rilanciare.
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
B=/e/soliton_simulator/controllo/CHI/triangolo
O=/e/soliton_simulator/controllo/girandola_blocchi
mkdir -p $O
MODO=$1; shift
ENV="env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
for Q in "$@"; do
  case "$Q" in t120|t120r28) DA0=6000;; t000) DA0=2000;; *) echo "scena sconosciuta $Q"; exit 2;; esac
  if [ "$MODO" = film ]; then
    U=$(ls $B/$Q/stato_*.npz | tail -1 | sed 's/.*stato_0*\([0-9]*\)\.npz/\1/'); echo "$Q $U" > $O/ultimo_$Q.txt
  else
    U=$(cut -d' ' -f2 $O/ultimo_$Q.txt)
  fi
  DA=$DA0
  while [ $DA -lt $U ]; do
    FI=$((DA + 2000)); [ $FI -gt $U ] && FI=$U
    T=$(printf "%s_%05d_%05d" $Q $DA $FI)
    if [ "$MODO" = film ]; then
      TXT=$O/girandola_film_$T.txt
      if ! grep -q "MB; .* stati" $TXT 2>/dev/null; then
        echo "$(date +%H:%M) film $T"
        $ENV $PY -u doc/referti_l2/film/esporta_film_triangolo_v3.py --quale $Q --da $DA --fino $FI --out $O/girandola_$T.npz > $TXT 2>&1 || { echo "FALLITO film $T"; exit 4; }
      fi
    else
      TXT=$O/girandola_chi_$(printf "%05d_%05d" $DA $FI)_$Q.txt
      if ! grep -q "^=====" <(tail -1 $TXT 2>/dev/null); then
        echo "$(date +%H:%M) giro $T"
        $ENV $PY -u doc/referti_l2/girandola_chi_v3.py giro --da $DA --fino $FI --scene $Q > $TXT 2>&1 || { echo "FALLITO giro $T"; exit 4; }
      fi
    fi
    DA=$FI
  done
done
echo "$(date +%H:%M) FINE $MODO"
