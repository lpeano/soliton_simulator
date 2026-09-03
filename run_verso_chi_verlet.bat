@echo off
REM Variante Velocity-Verlet dell'A/B verso chirale.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist out_vc mkdir out_vc
if not exist log mkdir log
for %%S in (%SEMI%) do (
 START "senza_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --chi-basc --verlet --csv out_vc\cond_senza_verlet_s%%S.csv --diaglog out_vc\diag_senza_verlet_s%%S.csv > log\senza_vc_verlet_s%%S.log 2>&1"
 START "con_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --chi-basc --verso-chi --verlet --csv out_vc\cond_con_verlet_s%%S.csv --diaglog out_vc\diag_con_verlet_s%%S.csv > log\con_vc_verlet_s%%S.log 2>&1"
)
echo A/B verso chirale Velocity-Verlet lanciato.
pause
