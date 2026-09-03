@echo off
REM ============================================================================
REM  TEST IPOTESI GUSCIO/CODA CHIRALE
REM  Misura nei diaglog: rchi_pos (raggio materia chi+1), rchi_neg (raggio
REM  spazio chi-1), rchi_ratio (>1 = chi-1 formano il guscio esterno),
REM  frac_chi_neg. Piu' rcom_/s2 gia' presenti.
REM  DOMANDA: nella fusione, le chi-1 vanno FUORI (guscio/coda) e le chi+1
REM           restano DENTRO (nuclei)? -> rchi_ratio cresce sopra 1.
REM  Condizione: default pieno (tutte le leggi standard) + pav-com, per vedere
REM  la fusione naturale. 3 semi, run LUNGO (la fusione avviene tardi).
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set SEMI=1 2 3

if not exist out_guscio mkdir out_guscio
if not exist out_video  mkdir out_video
if not exist log         mkdir log

echo === TEST GUSCIO/CODA CHIRALE (%NM% masse, %PASSI% passi, semi %SEMI%) ===
echo     misura rchi_pos/rchi_neg/rchi_ratio nella fusione
echo.

for %%S in (%SEMI%) do (
  START "gus_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --pav-com --csv out_guscio\cond_gus_s%%S.csv --diaglog out_guscio\diag_gus_s%%S.csv > log\gus_s%%S.log 2>&1"
)

START "video_gus_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %PASSI% --fps 24 --size 0.7,0.7,0.7 --sync --pav-com --out out_video\video_gus_s1.mp4 > log\video_gus_s1.log 2>&1"

echo Lanciati. Diaglog in out_guscio\, video in out_video\, log in log\.
echo Al ritorno: rchi_ratio sale sopra 1 nella fusione? (chi-1 = guscio/coda esterno)
echo Se troncano: set SEMI=1 e rilancia, poi 2, poi 3.
