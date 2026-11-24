#!/bin/bash
# ### [M0908-R] UNA CATENA DI CORSE DELLA CADUTA LIBERA, una dopo l'altra (il mandato di Luca 2026-11-22 09:08; la carta doc/TASK_HISTORY/2026-11-22_caduta_libera.md, sez. 2). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/caduta_lancia.sh V0 V3      (le varianti in fila): ognuna da k 0 a k 2000, gli stati ogni 250 in E:\soliton_simulator\controllo\CHI\caduta\<V>
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI/caduta
mkdir -p $O
REG=csv/solitone/_registro_corse.py
FORZA="Luca 2026-11-22 09:08: [M0908] la caduta libera, al piu' 5 processi nuovi, nel tetto dei 10"
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
for VAR in "$@"; do
  case "$VAR" in V0|V1|V2|V3|V4|V1m) ;; *) echo "variante sconosciuta $VAR"; exit 2;; esac
  V=caduta-$VAR
  if ! aperta $V; then
    $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/caduta_libera.py corsa --var $VAR --fino 2000 --registro $V" --note "La caduta libera $VAR (Luca 2026-11-22 09:08): un mattone al centro di S162, chi imposto e fermo lungo (0,1), 2000 tick; 1 filo, numba spento" --forza "$FORZA" || exit 3
  fi
  env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/caduta_libera.py corsa --var $VAR --fino 2000 --registro $V >> $O/log_$VAR.txt 2>&1
  rc=$?
  if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "k 2000 (uscita 0)"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_$VAR.txt)"; exit $rc; fi
done
exit 0
