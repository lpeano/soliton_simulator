@echo off
REM Variante Velocity-Verlet dell'A/B viriale.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist out_vir mkdir out_vir
if not exist log mkdir log
for %%S in (%SEMI%) do (
 START "voff_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --verlet --csv out_vir\cond_voff_verlet_s%%S.csv --diaglog out_vir\diag_voff_verlet_s%%S.csv > log\voff_vir_verlet_s%%S.log 2>&1"
 START "von_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --viriale --verlet --csv out_vir\cond_von_verlet_s%%S.csv --diaglog out_vir\diag_von_verlet_s%%S.csv > log\von_vir_verlet_s%%S.log 2>&1"
)
echo A/B viriale Velocity-Verlet lanciato.
pause
