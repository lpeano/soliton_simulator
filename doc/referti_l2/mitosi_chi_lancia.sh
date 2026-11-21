#!/bin/bash
# ### IL LANCIATORE DEI DUE RAMI DEL RAMO mitosi-chi (il mandato unico di Luca 2026-11-21 19:40, R4; la carta doc/TASK_HISTORY/2026-11-21_mitosi_chi.md, sez. 2). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/mitosi_chi_lancia.sh rami       dal primo scatto del tronco chi (E:\soliton_simulator\controllo\CHI\tronco\scatto.json): MITOSICHI (le nascite accese) e CHIEXT (spente), 20000 tick ciascuno, in parallelo
#   bash doc/referti_l2/mitosi_chi_lancia.sh riprendi   dopo un riavvio: i rami con la voce APERTA dal loro ultimo stato integro
# ### Lo chiama chi_lancia_tronco.sh del ramo lapse-u al primo scatto. I log in E:\soliton_simulator\controllo\mitosi_chi\.
MODO=$1
W=/c/Users/lpeano/wt_mitosi_chi
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/mitosi_chi
mkdir -p $O
REG=csv/solitone/_registro_corse.py
FORZA="Luca 2026-11-21 19:40: al primo scatto del tronco chi i due rami MITOSI-CHI e CHI-EXT in parallelo"
corri() { env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/mitosi_chi_v3.py "$@"; }
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }

apri() {   # NOME DA: la voce, prima delle corse (in sequenza: nessuna scrittura insieme nel registro)
  V=mitosi-chi-ramo-$1
  if ! aperta $V; then
    $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/mitosi_chi_v3.py ramo --nome $1 --da $2 --dopo 20000 --registro $V" --note "Il ramo $1 del ramo mitosi-chi dallo stato prima del primo scatto del tronco chi, 20000 tick (Luca 2026-11-21 19:40, R4); 1 filo, numba spento" --forza "$FORZA" || return 3
  fi
}

ramo() {   # NOME DA
  V=mitosi-chi-ramo-$1
  corri ramo --nome $1 --da $2 --dopo 20000 --registro $V >> $O/log_$1.txt 2>&1
  rc=$?
  if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "uscita 0"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_$1.txt)"; fi
  return $rc
}

if [ "$MODO" = "rami" ]; then
  apri MITOSICHI primo || exit 3
  apri CHIEXT primo || exit 3
  ramo MITOSICHI primo &
  P1=$!
  ramo CHIEXT primo &
  P2=$!
  wait $P1 $P2
  exit 0
fi
if [ "$MODO" = "riprendi" ]; then
  if aperta mitosi-chi-ramo-MITOSICHI; then ramo MITOSICHI ultimo & fi
  if aperta mitosi-chi-ramo-CHIEXT; then ramo CHIEXT ultimo & fi
  wait
  exit 0
fi
echo "uso: mitosi_chi_lancia.sh rami | riprendi"
exit 2
