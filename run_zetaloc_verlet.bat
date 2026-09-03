@echo off
REM Variante Velocity-Verlet dell'A/B smorzamento locale.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist out_zeta mkdir out_zeta
if not exist log mkdir log
for %%S in (%SEMI%) do (
 START "zoff_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --verlet --csv out_zeta\cond_zoff_verlet_s%%S.csv --diaglog out_zeta\diag_zoff_verlet_s%%S.csv > log\zoff_verlet_s%%S.log 2>&1"
 START "zon_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --kfrange 0 --zeta-loc --verlet --csv out_zeta\cond_zon_verlet_s%%S.csv --diaglog out_zeta\diag_zon_verlet_s%%S.csv > log\zon_verlet_s%%S.log 2>&1"
)
echo A/B zeta-loc Velocity-Verlet lanciato.
pause
