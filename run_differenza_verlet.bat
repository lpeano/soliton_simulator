@echo off
REM A/B diretto dell'integratore: stesso scenario, Eulero contro Velocity-Verlet.
set SIM=soliton_simulator.py
set PASSI=3000
set OGNI=5
if not exist out_test mkdir out_test
if not exist log mkdir log
START "eulero" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed 1 --passi %PASSI% --ogni %OGNI% --sync --csv out_test\cond_integratore_eulero.csv --diaglog out_test\diag_integratore_eulero.csv > log\integratore_eulero.log 2>&1"
START "verlet" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed 1 --passi %PASSI% --ogni %OGNI% --sync --verlet --csv out_test\cond_integratore_verlet.csv --diaglog out_test\diag_integratore_verlet.csv > log\integratore_verlet.log 2>&1"
echo A/B integratori lanciato: confrontare d_mean, vd, stress, Lz_orb e n_naninf.
pause
