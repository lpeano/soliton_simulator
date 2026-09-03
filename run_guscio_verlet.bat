@echo off
REM Variante Velocity-Verlet di run_guscio.bat.
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set SEMI=1 2 3
if not exist out_guscio mkdir out_guscio
if not exist log mkdir log
for %%S in (%SEMI%) do START "gus_verlet_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --pav-com --verlet --csv out_guscio\cond_gus_verlet_s%%S.csv --diaglog out_guscio\diag_gus_verlet_s%%S.csv > log\gus_verlet_s%%S.log 2>&1"
START "video_gus_verlet" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %PASSI% --fps 24 --size 0.7,0.7,0.7 --pav-com --verlet --out out_video\video_gus_verlet.mp4 > log\video_gus_verlet.log 2>&1"
echo Test guscio Velocity-Verlet lanciato.
pause
