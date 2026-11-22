#!/bin/bash
# ### IL TRONCO CHI DEL TRIANGOLO (P3 del mandato di Luca 2026-11-21 23:23; la carta doc/TASK_HISTORY/2026-11-21_triangolo_chi.md). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/triangolo_lancia.sh t120     (o t120r): dal tick 0 o dall'ultimo stato integro, fino al primo scatto (il limite k 200000)
QUALE=$1
case "$QUALE" in t120|t120r) ;; *) echo "uso: triangolo_lancia.sh t120 | t120r"; exit 2;; esac
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI/triangolo
mkdir -p $O
REG=csv/solitone/_registro_corse.py
V=chi-tronco-$QUALE
FORZA="Luca 2026-11-21 23:23: i due tronchi del triangolo ai primi posti liberi (opzione a)"
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
if ! aperta $V; then
  $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/triangolo_chi.py tronco --quale $QUALE --fino 200000 --registro $V" --note "Il tronco chi del triangolo $QUALE (le tre sfasate sul vuoto; t120r il gemello ruotato), chi curato (v2), niente bordo, fino al primo scatto (Luca 2026-11-21 23:23 e 23:30); 1 filo, numba spento" --forza "$FORZA" || exit 3
fi
env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/triangolo_chi.py tronco --quale $QUALE --fino 200000 --registro $V >> $O/log_$QUALE.txt 2>&1
rc=$?
if [ $rc -eq 10 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "il primo scatto (uscita 10): $(cat $O/$QUALE/scatto.json | cut -c1-200)"; elif [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FALLITO --punto "il limite k 200000 senza scatto: FERMO"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_$QUALE.txt)"; fi
exit $rc
