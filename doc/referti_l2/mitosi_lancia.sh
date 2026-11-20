#!/bin/bash
# ### IL LANCIATORE DEL TRONCO E DEI DUE RAMI (Luca 2026-11-20 18:40; la carta doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md del ramo primo-ordine, sez. 14). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/mitosi_lancia.sh nuovo       il tronco da C2 a k 3000; al primo scatto (uscita 10) i due rami in parallelo, 10000 tick ciascuno
#   bash doc/referti_l2/mitosi_lancia.sh riprendi    dopo un riavvio: cio' che era aperto riparte dall'ultimo stato integro (la tappa RIPRESA nel registro)
# ### Nel repo e non nello scratchpad: deve sopravvivere a un riavvio. I log in E:\soliton_simulator\controllo\mitosi_rami\.
MODO=$1
W=/c/Users/lpeano/wt_mitosi
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/mitosi_rami
mkdir -p $O
REG=csv/solitone/_registro_corse.py
FORZA="Luca 2026-11-20 18:40: il tronco, poi i due rami MITOSI e C2-EXT in parallelo"
corri() { env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/mitosi_rami.py "$@"; }
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }

ramo() {   # NOME DA
  V=mitosi-ramo-$1
  if ! aperta $V; then
    $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/mitosi_rami.py ramo --nome $1 --da $2 --dopo 10000 --registro $V" --note "Il ramo $1 dallo stato prima del primo scatto, 10000 tick (Luca 2026-11-20 18:40); 1 filo, numba spento" --forza "$FORZA" || return 3
  fi
  corri ramo --nome $1 --da $2 --dopo 10000 --registro $V >> $O/log_$1.txt 2>&1
  rc=$?
  if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "uscita 0"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_$1.txt)"; fi
  return $rc
}

rami() {   # DA
  ramo MITOSI $1 &
  P1=$!
  sleep 60
  ramo C2EXT $1 &
  P2=$!
  wait $P1 $P2
}

V=mitosi-tronco
if [ "$MODO" = "nuovo" ]; then
  $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/mitosi_rami.py tronco --da c2 --fino 40000 --registro $V" --note "Il tronco comune da C2 a k 3000 al primo scatto, le nascite spente (Luca 2026-11-20 18:40); 1 filo, numba spento" --forza "$FORZA" || exit 3
  DA=c2
elif [ "$MODO" = "riprendi" ]; then
  if [ -f $O/TRONCO/scatto.json ]; then
    DA_R=ultimo
    rami $DA_R
    exit $?
  fi
  aperta $V || { echo "il tronco non e' aperto nel registro e lo scatto non c'e': niente da riprendere"; exit 3; }
  DA=ultimo
else
  echo "uso: mitosi_lancia.sh nuovo|riprendi"; exit 2
fi
corri tronco --da $DA --fino 40000 --registro $V >> $O/log_TRONCO.txt 2>&1
rc=$?
if [ $rc -eq 10 ]; then
  $PY $REG chiudi --nome $V --esito FINITO --punto "il primo scatto (uscita 10): $(cat $O/TRONCO/scatto.json | cut -c1-200)"
  rami primo
  exit $?
fi
$PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc senza lo scatto (il log $O/log_TRONCO.txt)"
exit $rc
