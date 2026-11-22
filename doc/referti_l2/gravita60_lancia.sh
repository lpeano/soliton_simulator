#!/bin/bash
# ### [M1017-R] UNA DELLE DUE CORSE DEI DUE MATTONI A DISTANZA 60 (Luca 2026-11-22; la carta doc/TASK_HISTORY/2026-11-22_gravita_60.md). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/gravita60_lancia.sh on      (on o off): la coppia in fase, da k 0 fino a k 3000, gli stati ogni 250 in E:\soliton_simulator\controllo\CHI\due_corpi\F60-<on|off>
CH=$1; QUALE=F60-$CH
case "$CH" in on|off) ;; *) echo "uso: gravita60_lancia.sh on|off"; exit 2;; esac
W=/c/Users/lpeano/wt_lapse_u
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI/due_corpi
mkdir -p $O
REG=csv/solitone/_registro_corse.py
V=gravita-$QUALE
FORZA="Luca 2026-11-22: [M1017] le due corse a distanza 60 nel tetto dei 10, quando la CPU lo consente"
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
if ! aperta $V; then
  $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/gravita_due_corpi_d.py corsa --d 60 --chi $CH --fino 3000 --registro $V" --note "I due mattoni in fase a distanza 60 (Luca 2026-11-22, [M1017]): chi v2 (off: kappa 0, lo stesso c0), niente bordo, 3000 tick; 1 filo, numba spento" --forza "$FORZA" || exit 3
fi
env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/gravita_due_corpi_d.py corsa --d 60 --chi $CH --fino 3000 --registro $V >> $O/log_$QUALE.txt 2>&1
rc=$?
if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "k 3000 (uscita 0)"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_$QUALE.txt)"; fi
exit $rc
