@echo off
REM A/B diretto dell'integratore: stesso scenario, Eulero contro Velocity-Verlet.
set SIM=soliton_simulator.py
set PASSI=3000
set OGNI=5
if not exist log\test mkdir log\test
START "eulero" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed 1 --passi %PASSI% --ogni %OGNI% --sync --csv csv\test\cond_integratore_eulero.csv --diaglog csv\test\diag_integratore_eulero.csv > log\test\integratore_eulero.log 2>&1"
START "verlet" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed 1 --passi %PASSI% --ogni %OGNI% --sync --verlet --csv csv\test\cond_integratore_verlet.csv --diaglog csv\test\diag_integratore_verlet.csv > log\test\integratore_verlet.log 2>&1"
echo A/B integratori lanciato: confrontare d_mean, vd, stress, Lz_orb e n_naninf.
pause
