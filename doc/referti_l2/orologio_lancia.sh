#!/bin/bash
# ### [M1253-O] UNA CATENA DI CORSE DELL'OROLOGIO-MATTONE, una dopo l'altra (Luca 2026-11-22 12:53; la carta della caduta libera sez. 5). [[PROGETTO-MITOSI]]
#   bash doc/referti_l2/orologio_lancia.sh N1 Np NmV3      (le varianti in fila; 1000 tick ciascuna, gli stati e la fase in E:\soliton_simulator\controllo\CHI\caduta\orologio\<V>)
cd /c/Users/lpeano/wt_lapse_u || exit 3
O=/e/soliton_simulator/controllo/CHI/caduta/orologio
mkdir -p $O
for VAR in "$@"; do
  env -u PYTHONHOME -u PYTHONPATH PYTHONNOUSERSITE=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /e/python/py3132/python.exe -u doc/referti_l2/orologio_mattone.py corsa --var $VAR >> $O/log_$VAR.txt 2>&1 || { echo "FALLITO $VAR"; exit 4; }
  echo "$(date +%H:%M) FINITO $VAR"
done
