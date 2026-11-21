#!/bin/bash
# ### IL LANCIATORE DEL TRONCO CHI (il mandato unico di Luca 2026-11-21 19:40, T1; il task history doc/TASK_HISTORY/2026-11-21_lapse_u.md del ramo lapse-u, sez. 14). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/chi_lancia_tronco.sh attendi WINPID   aspetta l'uscita del lanciatore della corsa a k 20000 (chi_lancia_v2.sh, il suo processo Windows), poi decide dai FILE (chi_tronco.py decidi)
#   bash doc/referti_l2/chi_lancia_tronco.sh subito           decide dai file e, se si puo', lancia il tronco (la corsa a k 20000 gia' finita)
#   bash doc/referti_l2/chi_lancia_tronco.sh riprendi         dopo un riavvio: il tronco dal suo ultimo stato integro
# ### Al primo scatto (l'uscita 10): la voce chiusa FINITO, poi bash del lanciatore dei rami del ramo mitosi-chi. I log in E:\soliton_simulator\controllo\CHI\.
MODO=$1
W=/c/Users/lpeano/wt_lapse_u
WMC=/c/Users/lpeano/wt_mitosi_chi
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/CHI
LOG=$O/log_lancia_tronco.txt
mkdir -p $O
REG=csv/solitone/_registro_corse.py
V=chi-tronco
dice() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> $LOG; }
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }

tronco() {
  if ! aperta $V; then
    $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/chi_tronco.py corsa --da ultimo --fino 200000 --registro $V" --note "IL TRONCO CHI (Luca 2026-11-21 19:40, T1): la corsa del mattone con chi da k 20000 (o dall'ultimo stato del tronco) fino al primo arco a 2 pi, il limite k 200000; nascite spente; 1 filo, numba spento" || return 3
  fi
  dice "il tronco: chi_tronco.py corsa --da ultimo --fino 200000"
  env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/chi_tronco.py corsa --da ultimo --fino 200000 --registro $V >> $O/log_tronco.txt 2>&1
  rc=$?
  dice "il tronco e' uscito con $rc"
  if [ $rc -eq 10 ]; then
    $PY $REG chiudi --nome $V --esito FINITO --punto "il primo scatto (uscita 10): $(cat $O/tronco/scatto.json | cut -c1-200)"
    if [ -f $WMC/doc/referti_l2/mitosi_chi_lancia.sh ]; then
      dice "i rami: bash $WMC/doc/referti_l2/mitosi_chi_lancia.sh rami"
      bash $WMC/doc/referti_l2/mitosi_chi_lancia.sh rami
      return $?
    fi
    dice "FERMO: il lanciatore dei rami del ramo mitosi-chi NON c'e'"
    return 4
  fi
  if [ $rc -eq 0 ]; then
    $PY $REG chiudi --nome $V --esito FALLITO --punto "il limite k 200000 senza scatto: FERMO (Luca 2026-11-21 19:40); la proiezione in $O/proiezione_tronco.txt"
    env -u PYTHONHOME -u PYTHONPATH OMP_NUM_THREADS=1 $PY doc/referti_l2/chi_tronco.py proiezione > $O/proiezione_tronco.txt 2>&1
    dice "FERMO: il limite k 200000 senza scatto"
    return 0
  fi
  $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc senza lo scatto (il log $O/log_tronco.txt)"
  return $rc
}

decidi_e_vai() {
  D=$($PY doc/referti_l2/chi_tronco.py decidi)
  rc=$?
  dice "la decisione: $D (codice $rc)"
  if [ $rc -eq 20 ]; then tronco; return $?; fi
  dice "niente tronco"
  return 0
}

if [ "$MODO" = "attendi" ]; then
  dice "attendo il lanciatore della corsa a k 20000 (il processo Windows $2)"
  $PY doc/referti_l2/chi_tronco.py attendi $2 >> $LOG 2>&1
  decidi_e_vai
  exit $?
fi
if [ "$MODO" = "subito" ]; then decidi_e_vai; exit $?; fi
if [ "$MODO" = "riprendi" ]; then tronco; exit $?; fi
echo "uso: chi_lancia_tronco.sh attendi WINPID | subito | riprendi"
exit 2
