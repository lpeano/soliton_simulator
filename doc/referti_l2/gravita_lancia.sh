#!/bin/bash
# ### [M0417-R] UNA DELLE QUATTRO CORSE DEI DUE MATTONI (il test pulito della gravita', Luca 2026-11-22 04:17; la carta doc/TASK_HISTORY/2026-11-22_gravita_due_corpi.md). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/gravita_lancia.sh F on      (F o S; on o off): da k 0 fino a k 3000, gli stati ogni 250 in E:\soliton_simulator\controllo\CHI\due_corpi\<F-on>
SC=$1; CH=$2; QUALE=$SC-$CH
case "$QUALE" in F-on|F-off|S-on|S-off) ;; *) echo "uso: gravita_lancia.sh F|S on|off"; exit 2;; esac
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI/due_corpi
mkdir -p $O
REG=csv/solitone/_registro_corse.py
V=gravita-$QUALE
FORZA="Luca 2026-11-22 04:17: [M0417] le quattro corse dei due mattoni nel tetto dei 10"
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
if ! aperta $V; then
  $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/gravita_due_corpi.py corsa --scena $SC --chi $CH --fino 3000 --registro $V" --note "I due mattoni $QUALE (il test pulito della gravita', Luca 2026-11-22 04:17): la distanza 39 lungo un asse, chi v2 (off: kappa 0, lo stesso c0), niente bordo, 3000 tick; 1 filo, numba spento" --forza "$FORZA" || exit 3
fi
env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/gravita_due_corpi.py corsa --scena $SC --chi $CH --fino 3000 --registro $V >> $O/log_$QUALE.txt 2>&1
rc=$?
if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "k 3000 (uscita 0)"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_$QUALE.txt)"; fi
exit $rc
