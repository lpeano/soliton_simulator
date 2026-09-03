@echo off
REM TEST PRECESSIONE: verso azimutale da radiale x spinore --ls-azim.
REM Un solo run: seed 1, sep=10, 700 passi. Non lancia sei processi.
set SIM=soliton_simulator.py
set SEED=1
set PASSI=700
set OGNI=5
set DBOGNI=100
set SEP=10
set CATENA=--verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett
if not exist out_elast mkdir out_elast
if not exist log mkdir log
python %SIM% --batch --nmasse 3 --sep %SEP% --seed %SEED% --passi %PASSI% --ogni %OGNI% %CATENA% --ls-azim --sync-db out_elast\db_ls_azim_sep10_s%SEED%.pkl --db-ogni %DBOGNI% --csv out_elast\cond_ls_azim_sep10_s%SEED%.csv --diaglog out_elast\ls_azim_sep10_s%SEED%.csv > log\ls_azim_sep10_s%SEED%.log 2>&1
echo Test ls-azim completato. Dati in out_elast\, log in log\.
pause
