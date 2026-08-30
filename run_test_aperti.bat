@echo off
REM ============================================================================
REM  I TEST APERTI — 3 masse, run lungo, metriche COVARIANTI nel diaglog
REM  Condizioni per seme (ciascuna isola una domanda aperta):
REM    base      : niente                    -> riferimento
REM    sync      : --sync                     -> l'accoppiamento asimmetrico conta sul lungo?
REM    virz      : --viriale --zeta-vir       -> freno anisotropo: Lz_orb concorde? rcom~s2^(2/3)/(1-s2)?
REM    pav       : --pav-com                  -> quanto il muro 0.05 falsava il pavimento?
REM    tutto     : --sync --viriale --zeta-vir --pav-com --chi-basc  -> tutta la fisica insieme
REM  Tutte con --diaglog: cattura tw_q, sync_rel, d0_disp, s2, rcom, rchi, guscio_idx (covarianti)
REM  ANALISI al ritorno: SOLO metriche covarianti, correlazioni forti e concordi sui 3 semi.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set SEMI=1 2 3

if not exist out_test mkdir out_test
if not exist log       mkdir log

echo === TEST APERTI (%NM% masse, %PASSI% passi, semi %SEMI%) ===
echo     base / sync / virz / pav / tutto  -- metriche covarianti
echo.

for %%S in (%SEMI%) do (
  START "base_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI%                                                    --csv out_test\cond_base_s%%S.csv  --diaglog out_test\diag_base_s%%S.csv  > log\base_s%%S.log 2>&1"
  START "sync_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync                                             --csv out_test\cond_sync_s%%S.csv  --diaglog out_test\diag_sync_s%%S.csv  > log\sync_s%%S.log 2>&1"
  START "virz_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --viriale --zeta-vir                               --csv out_test\cond_virz_s%%S.csv  --diaglog out_test\diag_virz_s%%S.csv  > log\virz_s%%S.log 2>&1"
  START "pav_s%%S"   /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --pav-com                                          --csv out_test\cond_pav_s%%S.csv   --diaglog out_test\diag_pav_s%%S.csv   > log\pav_s%%S.log 2>&1"
  START "tutto_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --viriale --zeta-vir --pav-com --chi-basc    --csv out_test\cond_tutto_s%%S.csv --diaglog out_test\diag_tutto_s%%S.csv > log\tutto_s%%S.log 2>&1"
)

echo Lanciati. Diaglog in out_test\, log in log\.
echo ATTENZIONE memoria: 15 batch in parallelo. Se troncano: set SEMI=1 e rilancia, poi 2, poi 3.
echo   (oppure riduci le condizioni: commenta le righe che non ti servono subito)
