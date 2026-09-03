@echo off
REM TEST INVARIANZA DI SCALA: stessa legge C=100 a due numeri di masse.
set SIM=soliton_simulator.py
set PASSI=4000
set OGNI=5
set DBOGNI=100
if not exist out_elast mkdir out_elast
if not exist log mkdir log
START "scala_piccola" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 4 --seed 1 --passi %PASSI% --ogni %OGNI% --verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --elast-c 100 --sync-db out_elast\db_scala_piccola.pkl --db-ogni %DBOGNI% --csv out_elast\cond_scala_piccola.csv --diaglog out_elast\scala_piccola.csv > log\scala_piccola.log 2>&1"
START "scala_grande" /MIN cmd /c "python %SIM% --batch --nmasse 6 --sep 4 --seed 1 --passi %PASSI% --ogni %OGNI% --verlet --sync --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --calore-vett --elast-c 100 --sync-db out_elast\db_scala_grande.pkl --db-ogni %DBOGNI% --csv out_elast\cond_scala_grande.csv --diaglog out_elast\scala_grande.csv > log\scala_grande.log 2>&1"
echo Test invarianza di scala lanciato con catena completa: confrontare osservabili normalizzate.
pause
