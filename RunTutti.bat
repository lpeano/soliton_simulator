@echo off
REM =============================================================================
REM  run_tutti.bat - esegue TUTTI i test batch e i video a 10000 passi in parallelo.
REM  Windows.  Uso:  run_tutti.bat
REM
REM  Canonico: soliton_simulator.py (determ + forma pura + calcio vettoriale di default).
REM  Il diaglog scrive AUTOMATICAMENTE anche le colonne del test gauge emergente:
REM    centro_N/coer/cosphi  (struttura collettiva al centro: cosphi<0 = antifase)
REM    guscio_N/coer/cosphi/circ  (buccia attorno alle masse; circ = olonomia = firma gauge)
REM  Ogni processo parte in una finestra separata (START) = esecuzione in parallelo.
REM =============================================================================

setlocal
set SIM=soliton_simulator.py
set PASSI=20000
set FRAMES=20000
set SEP=16
if not exist out_test  mkdir out_test
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === Avvio di tutti i test in parallelo (20000 passi) ===
echo     Ogni test apre una finestra separata. Log in .\log\
echo.

REM ============ 2 MASSE ============
@START "2m_default" /MIN cmd /c "python %SIM% --batch --nmasse 2 --sep %SEP% --passi %PASSI% --ogni 5 --sync --csv out_test\cond_2m_default.csv --diaglog out_test\diag_2m_default.csv > log\2m_default.log 2>&1"
@REM START "2m_scalare" /MIN cmd /c "python %SIM% --batch --nmasse 2 --sep %SEP% --passi %PASSI% --ogni 5 --calore-scal --csv out_test\cond_2m_scalare.csv --diaglog out_test\diag_2m_scalare.csv > log\2m_scalare.log 2>&1"
@REM START "2m_d0" /MIN cmd /c "python %SIM% --batch --nmasse 2 --sep %SEP% --passi %PASSI% --ogni 5 --tau-d0 --csv out_test\cond_2m_d0.csv --diaglog out_test\diag_2m_d0.csv > log\2m_d0.log 2>&1"
@REM START "2m_video_default" /MIN cmd /c "python %SIM% --test "N-MASSE" --nmasse 2 --sep %SEP% --giri 0 --ppf 1 --frames %FRAMES% --fps 24 --out out_video\2m_default.mp4 > log\2m_default_video.log 2>&1"
@REM START "2m_video_d0" /MIN cmd /c "python %SIM% --test "N-MASSE" --nmasse 2 --sep %SEP% --giri 0 --ppf 1 --frames %FRAMES% --fps 24 --tau-d0 --out out_video\2m_d0.mp4 > log\2m_d0_video.log 2>&1"

REM ============ 3 MASSE ============
START "3m_default" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --passi %PASSI% --ogni 5 --sync --csv out_test\cond_3m_default.csv --diaglog out_test\diag_3m_default.csv > log\3m_default.log 2>&1"
@REM START "3m_scalare" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --passi %PASSI% --ogni 5 --calore-scal --csv out_test\cond_3m_scalare.csv --diaglog out_test\diag_3m_scalare.csv > log\3m_scalare.log 2>&1"
@REM START "3m_d0" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep %SEP% --passi %PASSI% --ogni 5 --tau-d0 --csv out_test\cond_3m_d0.csv --diaglog out_test\diag_3m_d0.csv > log\3m_d0.log 2>&1"
START "3m_video_default" /MIN cmd /c "python %SIM% --test "N-MASSE" --nmasse 3 --sep %SEP% --giri 0 --ppf 1 --frames %FRAMES% --fps 24 --sync --out out_video\3m_default.mp4 > log\3m_default_video.log 2>&1"
@REM START "3m_video_d0" /MIN cmd /c "python %SIM% --test "N-MASSE" --nmasse 3 --sep %SEP% --giri 0 --ppf 1 --frames %FRAMES% --fps 24 --tau-d0 --out out_video\3m_d0.mp4 > log\3m_d0_video.log 2>&1"

echo.
echo === Tutti i test lanciati in finestre separate (parallelo). ===
echo     Risultati:  out_test\ (CSV)   out_video\ (mp4)   log\ (log)
echo     Le finestre si chiudono da sole a fine test.
pause
endlocal