@echo off
REM TEST DIAGNOSTICO: circolazione topologica sui cicli del grafo.
REM Un solo run: non usa coordinate/embedding per costruire i cicli e non modifica la dinamica.
set SIM=soliton_simulator.py
set SEED=1
set PASSI=300
set OGNI=5
set DBOGNI=100
set SEP=10
if not exist out_elast mkdir out_elast
if not exist log mkdir log
python %SIM% --batch --nmasse 3 --sep %SEP% --seed %SEED% --passi %PASSI% --ogni %OGNI% --sync --verlet --sync-db out_elast\db_circolazione_topologica_s%SEED%.pkl --db-ogni %DBOGNI% --csv out_elast\cond_circolazione_topologica_s%SEED%.csv --diaglog out_elast\circolazione_topologica_s%SEED%.csv > log\circolazione_topologica_s%SEED%.log 2>&1
echo Test circolazione topologica completato.
echo Dati: out_elast\circolazione_topologica_s%SEED%.csv
 echo Log: log\circolazione_topologica_s%SEED%.log
 echo Colonne: n_cicli_topologici, circolazione_topologica_max, circolazione_topologica_media_assoluta, circolazione_topologica_media.
pause
