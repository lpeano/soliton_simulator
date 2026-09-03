@echo off
REM =============================================================================
REM  run_kfrange.bat - A/B del CANALE ORBITALE (K_FRANGE) in parallelo.
REM  Windows. Lancia dalla cartella che contiene soliton_simulator.py:  run_kfrange.bat
REM
REM  Domanda del test: il canale orbitale (moto lungo le frange) ACCENDE la
REM  precessione, si' o no? K_FRANGE=0 (spento, riferimento) vs K_FRANGE=%KF% (sonda).
REM
REM  REGOLE FERREE (guardiano):
REM   - La PROVA sta nei diaglog (Lz_orb), da giudicare nella finestra PRE-COLLASSO.
REM   - Conta come segnale solo se il verso e' CONCORDE su >=3 semi -> per questo i
REM     batch girano su tutti i semi. I video sono per l'OCCHIO (bastano 1-2).
REM   - Camera FISSA nei video (--giri 0): la "rotazione" da camera auto e' un
REM     artefatto gia' preso in faccia. Con --giri 0 ogni rotazione che vedi e' vera.
REM   - 0.03 e' un NUMERO-SONDA, non una legge: risultati etichettati
REM     'in-verifica con parametro libero', mai 'dimostrato'.
REM
REM  CARICO: 6 batch + 2 video = 8 processi paralleli pesanti. Se la macchina e'
REM  modesta, riduci SEMI (es. "1 2") o commenta (REM) le righe video.
REM =============================================================================

setlocal
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set FRAMES=20000
set FPS=24
set OGNI=5
set KF=0.03
set SEMI=1 2 3

if not exist out_test  mkdir out_test
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === A/B canale orbitale K_FRANGE ===
echo     %NM% masse, sep %SEP%, %PASSI% passi ^| spento(0) vs sonda(%KF%) ^| semi: %SEMI%
echo     Ogni run in una finestra separata (parallelo). Log in .\log\
echo.

REM ================= BATCH: la PROVA numerica (CSV + diaglog), su TUTTI i semi =================
for %%S in (%SEMI%) do (
  START "batch_kf0_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange 0   --csv out_test\cond_kf0_s%%S.csv --diaglog out_test\diag_kf0_s%%S.csv > log\batch_kf0_s%%S.log 2>&1"
  START "batch_kf_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --kfrange %KF% --csv out_test\cond_kf_s%%S.csv  --diaglog out_test\diag_kf_s%%S.csv  > log\batch_kf_s%%S.log 2>&1"
)

REM ================= VIDEO: l'OCCHIO (camera FISSA --giri 0), seed 1 spento+acceso =================
REM  (per allineare meglio occhio<->numeri, --size uguale su entrambi. Restano corse
REM   gemelle non identiche: video=guarda, diaglog=misura.)
START "video_kf0_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --sync --kfrange 0   --out out_video\video_kf0_s1.mp4 > log\video_kf0_s1.log 2>&1"
START "video_kf_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --sync --kfrange %KF% --out out_video\video_kf_s1.mp4 > log\video_kf_s1.log 2>&1"

echo.
echo === Lanciati. ===
echo     out_test\  : cond_*.csv (condensazione) + diag_*.csv (diaglog = la PROVA, Lz_orb)
echo     out_video\ : video_*.mp4 (camera fissa)
echo     log\       : output per run (se qualcosa non parte, guarda qui)
echo     Le finestre si chiudono da sole a fine run.
pause
endlocal
