@echo off
REM Variante Velocity-Verlet dei test aperti con DB.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set DBOGNI=100
set SEMI=1 2 3
if not exist out_test mkdir out_test
if not exist log mkdir log
for %%S in (%SEMI%) do START "tutto_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --viriale --zeta-vir --pav-com --chi-basc --verlet --sync-db out_test\db_tutto_verlet_s%%S.pkl --db-ogni %DBOGNI% --csv out_test\cond_tutto_verlet_s%%S.csv --diaglog out_test\diag_tutto_verlet_s%%S.csv > log\tutto_verlet_s%%S.log 2>&1"
echo Test aperti Velocity-Verlet lanciato.
pause
