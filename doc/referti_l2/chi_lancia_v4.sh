#!/bin/bash
# ### LA CORSA NUOVA DEL MATTONE CON CHI CURATO (V4 del mandato di Luca 2026-11-21 23:30; la carta doc/TASK_HISTORY/2026-11-21_lorentz_locale.md, sez. 4). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/chi_lancia_v4.sh nuova      da k 0 di C2 (come la vecchia) fino a k 20000, gli stati in E:\soliton_simulator\controllo\CHI\mattone_v2
#   bash doc/referti_l2/chi_lancia_v4.sh riprendi   dall'ultimo stato integro di mattone_v2
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI
REG=csv/solitone/_registro_corse.py
V=chi-mattone-v2
FORZA="Luca 2026-11-21 23:30: V4, la corsa nuova del mattone con chi curato al primo posto libero"
DA=""
if [ "$1" = "riprendi" ]; then DA="--da $(ls $O/mattone_v2/stato_*.npz | tail -1 | sed 's#^/e/#E:/#')"; fi
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
if ! aperta $V; then
  $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/chi_mattone_v3.py corsa --fino 20000 $DA --registro $V" --note "Il mattone con chi CURATO (l'inerzia f: v_chi = la luce; kappa il numero) da k 0 di C2 come la vecchia fino a k 20000 (Luca 2026-11-21 23:30, V4); 1 filo, numba spento" --forza "$FORZA" || exit 3
fi
env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/chi_mattone_v3.py corsa --fino 20000 $DA --registro $V >> $O/log_mattone_v2.txt 2>&1
rc=$?
if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "uscita 0"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_mattone_v2.txt)"; fi
exit $rc
