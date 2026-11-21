#!/bin/bash
# ### IL LANCIATORE DELLA PARTE C DEL CAMPO CHI (Luca 2026-11-21 15:57 e 17:30; il task history doc/TASK_HISTORY/2026-11-21_lapse_u.md del ramo lapse-u, sez. 9.4 e 11). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/chi_lancia.sh      il registro (apri), la corsa da k 0 a k 3000, il registro (chiudi); il log in E:\soliton_simulator\controllo\CHI\log_mattone.txt
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI
mkdir -p $O
REG=csv/solitone/_registro_corse.py
V=chi-mattone
$PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/chi_mattone.py corsa --fino 3000 --registro $V" --note "La parte C: il mattone di C2 col campo chi, 3000 tick da k 0 (Luca 2026-11-21 15:57 e 17:30); 1 filo, numba spento" || exit 3
env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/chi_mattone.py corsa --fino 3000 --registro $V >> $O/log_mattone.txt 2>&1
rc=$?
if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "uscita 0"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_mattone.txt)"; fi
exit $rc
