#!/bin/bash
# ### LA RIPARTENZA DEL RAMO MITOSI COL CODICE V2 (l'orientamento ereditato; C4 del mandato di Luca 2026-11-21 23:13; la carta doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md, sez. 4). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/mitosi_lancia_v3.sh riparti     da MITOSI/stato_36250 (sha1 64999c5b) fino a k 45976 (la fine del ramo di prima), gli stati in MITOSI_V2
#   bash doc/referti_l2/mitosi_lancia_v3.sh riprendi    dopo un riavvio: dall'ultimo stato integro di MITOSI_V2
# ### La voce vecchia mitosi-ramo-MITOSI resta FALLITO. Il log in E:\soliton_simulator\controllo\mitosi_rami\log_MITOSI_V2.txt
MODO=$1
W=/c/Users/lpeano/wt_mitosi
cd $W || exit 3
PY=/e/python/py3132/python.exe
O=/e/soliton_simulator/controllo/mitosi_rami
REG=csv/solitone/_registro_corse.py
V=mitosi-ramo-MITOSI-v2
FORZA="Luca 2026-11-21 23:13: C4, il ramo MITOSI riparte da k 36250 col codice nuovo se le prove passano"
corri() { env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 TMP='E:\python\tmp' TEMP='E:\python\tmp' $PY -u doc/referti_l2/mitosi_rami_v2.py "$@"; }
aperta() { $PY -c "import sys; sys.path[:0]=['csv/solitone','csv']; import _registro_corse as R; sys.exit(0 if '$1' in R.aperte() else 1)"; }
if [ "$MODO" = "riparti" ]; then F=E:/soliton_simulator/controllo/mitosi_rami/MITOSI/stato_36250.npz; fi
if [ "$MODO" = "riprendi" ]; then F=$(ls $O/MITOSI_V2/stato_*.npz | tail -1); fi
[ -n "$F" ] || { echo "uso: mitosi_lancia_v3.sh riparti | riprendi"; exit 2; }
if ! aperta $V; then
  $PY $REG apri --nome $V --tipo lunga --comando "E:/python/py3132/python.exe doc/referti_l2/mitosi_rami_v2.py riparti --da $F --fino 45976 --nome MITOSI_V2 --registro $V" --note "Il ramo MITOSI riparte col codice nuovo (l'orientamento ereditato) da k 36250 fino a k 45976 (Luca 2026-11-21 23:13, C4; le prove O1-O8 passate); la voce vecchia resta FALLITO; 1 filo, numba spento" --forza "$FORZA" || exit 3
fi
corri riparti --da $F --fino 45976 --nome MITOSI_V2 --registro $V >> $O/log_MITOSI_V2.txt 2>&1
rc=$?
if [ $rc -eq 0 ]; then $PY $REG chiudi --nome $V --esito FINITO --punto "uscita 0"; else $PY $REG chiudi --nome $V --esito FALLITO --punto "uscita $rc (il log $O/log_MITOSI_V2.txt)"; fi
exit $rc
