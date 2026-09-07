@echo off
REM Variante Velocity-Verlet dell'A/B polo maturo.
set SIM=soliton_simulator.py
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist log\pm mkdir log\pm
for %%S in (%SEMI%) do (
 START "base_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --verlet --csv csv\pm\cond_base_verlet_s%%S.csv --diaglog csv\pm\diag_base_verlet_s%%S.csv > log\pm\base_verlet_s%%S.log 2>&1"
 START "polo_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --polo-maturo --verlet --csv csv\pm\cond_polo_verlet_s%%S.csv --diaglog csv\pm\diag_polo_verlet_s%%S.csv > log\pm\polo_verlet_s%%S.log 2>&1"
)
echo A/B polo maturo Velocity-Verlet lanciato.
pause
