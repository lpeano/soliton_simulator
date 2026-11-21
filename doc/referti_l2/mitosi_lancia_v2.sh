#!/bin/bash
# ### IL LANCIATORE DELLA PROROGA (la nota di Luca 2026-11-21 13:57; la carta doc/TASK_HISTORY/2026-11-20_covariante_di_stella.md del ramo primo-ordine, sez. 16). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/mitosi_lancia_v2.sh attendi WINPID   aspetta che il lanciatore in corso (mitosi_lancia.sh, il suo processo Windows) esca; poi decide dai FILE:
#                                                            scatto.json c'e' -> niente (i rami li ha fatti il lanciatore vecchio); l'ultimo stato e' k 40000 -> la PROROGA fino a k 50000; altrimenti niente, e lo scrive
#   bash doc/referti_l2/mitosi_lancia_v2.sh riprendi         dopo un riavvio (sostituisce mitosi_lancia.sh riprendi da qui in avanti)
# ### mitosi_lancia.sh NON si tocca (e' in uso). I log in E:\soliton_simulator\controllo\mitosi_rami\.
MODO=$1
W=/c/Users/lpeano/wt_mitosi
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/mitosi_rami
LOG=$O/log_PROROGA.txt
mkdir -p $O
REG=csv/solitone/_registro_corse.py
FORZA="Luca 2026-11-20 18:40: il tronco, poi i due rami MITOSI e C2-EXT in parallelo; la proroga del tronco Luca 2026-11-21 13:57"
VT=mitosi-tronco
VP=mitosi-tronco-proroga
K1=40000
K2=50000
corri() { env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/mitosi_rami.py "$@"; }
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
dice() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> $LOG; }

ramo() {   # NOME DA (come mitosi_lancia.sh)
  V=mitosi-ramo-$1
  if ! aperta $V; then
    $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/mitosi_rami.py ramo --nome $1 --da $2 --dopo 10000 --registro $V" --note "Il ramo $1 dallo stato prima del primo scatto, 10000 tick (Luca 2026-11-20 18:40; lanciato da mitosi_lancia_v2.sh, la proroga Luca 2026-11-21 13:57); 1 filo, numba spento" --forza "$FORZA" || return 3
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

proroga() {   # la voce nuova e il tronco da k 40000 (o dall'ultimo suo stato, dopo un riavvio) fino a k 50000
  if ! aperta $VP; then
    $PY $REG apri --nome $VP --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/mitosi_rami.py tronco --da ultimo --fino $K2 --registro $VP" --note "LA PROROGA del tronco da k $K1 a k $K2 (Luca 2026-11-21 13:57): a k $K1 nessuno scatto; la voce $VT chiusa FALLITO dal lanciatore vecchio (mitosi_lancia.sh, in uso, non toccato) e' IL LIMITE, non un guasto; la ripresa al bit dallo stato k $K1; 1 filo, numba spento" || return 3
  fi
  dice "la proroga: tronco --da ultimo --fino $K2"
  corri tronco --da ultimo --fino $K2 --registro $VP >> $O/log_TRONCO.txt 2>&1
  rc=$?
  dice "la proroga e' uscita con $rc"
  if [ $rc -eq 10 ]; then
    $PY $REG chiudi --nome $VP --esito FINITO --punto "il primo scatto nella proroga (uscita 10): $(cat $O/TRONCO/scatto.json | cut -c1-200)"
    rami primo
    return $?
  fi
  if [ $rc -eq 0 ]; then
    $PY $REG chiudi --nome $VP --esito FALLITO --punto "il limite k $K2 senza scatto: FERMO (Luca 2026-11-21 13:57); la proiezione aggiornata in $O/proiezione_k$K2.txt"
    env -u PYTHONHOME -u PYTHONPATH OMP_NUM_THREADS=1 $PY doc/referti_l2/mitosi_ritmo_contatore.py --base $O --fino $K2 > $O/proiezione_k$K2.txt 2>&1
    dice "FERMO: il limite k $K2 senza scatto; la proiezione in $O/proiezione_k$K2.txt"
    return 0
  fi
  $PY $REG chiudi --nome $VP --esito FALLITO --punto "uscita $rc senza lo scatto (il log $O/log_TRONCO.txt)"
  return $rc
}

dopo_tronco() {   # la decisione dai file, dopo che il tronco fino a k 40000 e' finito
  D=$($PY doc/referti_l2/mitosi_attendi.py decidi $O/TRONCO $K1)
  rc=$?
  dice "la decisione: $D (codice $rc)"
  if [ $rc -eq 20 ]; then proroga; return $?; fi
  if [ $rc -eq 0 ]; then dice "lo scatto c'e': niente da fare (i rami li fa il lanciatore che ha visto lo scatto)"; return 0; fi
  dice "nessuno scatto e l'ultimo stato NON e' k $K1: il tronco e' caduto prima; NIENTE proroga, si riprende a mano"
  return $rc
}

if [ "$MODO" = "attendi" ]; then
  dice "attendo il lanciatore (il processo Windows $2)"
  $PY doc/referti_l2/mitosi_attendi.py attendi $2 >> $LOG 2>&1
  dopo_tronco
  exit $?
elif [ "$MODO" = "riprendi" ]; then
  if [ -f $O/TRONCO/scatto.json ]; then
    dice "riprendi: lo scatto c'e', i rami dall'ultimo loro stato"
    rami ultimo
    exit $?
  fi
  if aperta $VP; then
    dice "riprendi: la proroga e' aperta"
    proroga
    exit $?
  fi
  if aperta $VT; then
    dice "riprendi: il tronco fino a k $K1"
    corri tronco --da ultimo --fino $K1 --registro $VT >> $O/log_TRONCO.txt 2>&1
    rc=$?
    if [ $rc -eq 10 ]; then
      $PY $REG chiudi --nome $VT --esito FINITO --punto "il primo scatto (uscita 10): $(cat $O/TRONCO/scatto.json | cut -c1-200)"
      rami primo
      exit $?
    fi
    if [ $rc -eq 0 ]; then
      $PY $REG chiudi --nome $VT --esito FINITO --punto "il limite k $K1 senza scatto: segue la proroga (Luca 2026-11-21 13:57)"
    else
      $PY $REG chiudi --nome $VT --esito FALLITO --punto "uscita $rc senza lo scatto (il log $O/log_TRONCO.txt)"
    fi
    dopo_tronco
    exit $?
  fi
  dice "riprendi: niente di aperto e nessuno scatto: niente da riprendere"
  exit 3
else
  echo "uso: mitosi_lancia_v2.sh attendi WINPID | riprendi"; exit 2
fi
