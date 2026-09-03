@echo off
REM Variante Velocity-Verlet del run generale Windows.
set SIM=soliton_simulator.py
set PASSI=20000
if not exist out_test mkdir out_test
if not exist out_video mkdir out_video
if not exist log mkdir log
START "2m_verlet" /MIN cmd /c "python %SIM% --batch --nmasse 2 --sep 16 --passi %PASSI% --ogni 5 --verlet --csv out_test\cond_2m_verlet.csv --diaglog out_test\diag_2m_verlet.csv > log\2m_verlet.log 2>&1"
START "3m_verlet" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 16 --passi %PASSI% --ogni 5 --verlet --csv out_test\cond_3m_verlet.csv --diaglog out_test\diag_3m_verlet.csv > log\3m_verlet.log 2>&1"
START "2m_video_verlet" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse 2 --sep 16 --giri 0 --ppf 1 --frames %PASSI% --fps 24 --verlet --out out_video\2m_verlet.mp4 > log\2m_video_verlet.log 2>&1"
START "3m_video_verlet" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse 3 --sep 16 --giri 0 --ppf 1 --frames %PASSI% --fps 24 --verlet --out out_video\3m_verlet.mp4 > log\3m_video_verlet.log 2>&1"
echo Run generale Velocity-Verlet lanciato.
pause
