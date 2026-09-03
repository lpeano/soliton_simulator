@echo off
REM Variante Velocity-Verlet di run_ordine_spin.bat.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist out_spin mkdir out_spin
if not exist log mkdir log
for %%S in (%SEMI%) do START "spin_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 8 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --verlet --csv out_spin\cond_spin_verlet_s%%S.csv --diaglog out_spin\diag_spin_verlet_s%%S.csv > log\spin_verlet_s%%S.log 2>&1"
echo Test ordine spin Velocity-Verlet lanciato.
pause
