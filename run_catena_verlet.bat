@echo off
REM Variante Velocity-Verlet di run_catena.bat. Eulero resta nello script originale.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set DBOGNI=100
if not exist out_cat mkdir out_cat
if not exist log mkdir log
START "catena_verlet" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 3.9 --seed 42 --passi %PASSI% --ogni %OGNI% --viriale --olon-part --polo-maturo --sync --calore-vett --verlet --sync-db out_cat\db_verlet.pkl --db-ogni %DBOGNI% --csv out_cat\cond_verlet.csv --diaglog out_cat\diag_verlet.csv > log\catena_verlet.log 2>&1"
START "catena_verlet_sep7" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 7 --seed 42 --passi %PASSI% --ogni %OGNI% --viriale --olon-part --polo-maturo --sync --calore-vett --verlet --sync-db out_cat\db_verlet_sep7.pkl --db-ogni %DBOGNI% --csv out_cat\cond_verlet_sep7.csv --diaglog out_cat\diag_verlet_sep7.csv > log\catena_verlet_sep7.log 2>&1"
echo Catena Velocity-Verlet lanciata. Risultati in out_cat\ e log\.
pause
