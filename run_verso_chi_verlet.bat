@echo off
REM Variante Velocity-Verlet dell'A/B verso chirale.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist log\vc mkdir log\vc
for %%S in (%SEMI%) do (
 START "senza_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --verlet --csv csv\vc\cond_senza_verlet_s%%S.csv --diaglog csv\vc\diag_senza_verlet_s%%S.csv > log\vc\senza_vc_verlet_s%%S.log 2>&1"
 START "con_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --verso-chi --verlet --csv csv\vc\cond_con_verlet_s%%S.csv --diaglog csv\vc\diag_con_verlet_s%%S.csv > log\vc\con_vc_verlet_s%%S.log 2>&1"
)
echo A/B verso chirale Velocity-Verlet lanciato.
pause
