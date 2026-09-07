@echo off
REM Variante Velocity-Verlet dell'A/B K_FRANGE.
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set KF=0.03
set SEMI=1 2 3
if not exist log\test mkdir log\test
for %%S in (%SEMI%) do (
 START "kf0_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0 --verlet --csv csv\test\cond_kf0_verlet_s%%S.csv --diaglog csv\test\diag_kf0_verlet_s%%S.csv > log\test\kf0_verlet_s%%S.log 2>&1"
 START "kf_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange %KF% --verlet --csv csv\test\cond_kf_verlet_s%%S.csv --diaglog csv\test\diag_kf_verlet_s%%S.csv > log\test\kf_verlet_s%%S.log 2>&1"
)
echo A/B K_FRANGE Velocity-Verlet lanciato.
pause
