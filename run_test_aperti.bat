@echo off
REM ============================================================================
REM  TEST APERTI con DB (idempotente+versionato) — 3 masse, run lungo
REM  Attivo: solo TUTTO (le altre condizioni commentate come nel tuo file).
REM  DB: un file PER seme (out_test\db_tutto_s%%S.pkl). Serve a SPEZZARE i run:
REM    - 1a esecuzione: parte da zero, salva ogni 1000 passi nel suo DB.
REM    - se interrotto: RILANCI lo stesso .bat -> ogni run CARICA il suo DB e continua.
REM    - per ripartire pulito: aggiungi --db-cleanup (o cancella i .pkl a mano).
REM  NB: il DB e' rifiutato se cambi il codice (hash diverso) -> allora --db-cleanup.
REM  NB2: il tracking-masse non e' nel DB: dopo un resume le colonne m0_/dist_
REM       potrebbero rietichettare le masse. La FISICA riprende identica (idempotente).
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set FRAMES=20000
set FPS=24
set OGNI=5
set SEMI=1 2 3

if not exist out_test  mkdir out_test
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === TEST APERTI con DB (%NM% masse, %PASSI% passi, semi %SEMI%) ===
echo     solo TUTTO attivo, DB per seme (spezzabile)
echo.

REM ================= BATCH (con DB per seme) =================
for %%S in (%SEMI%) do (
  @REM START "base_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI%                                                    --sync-db out_test\db_base_s%%S.pkl  --csv out_test\cond_base_s%%S.csv  --diaglog out_test\diag_base_s%%S.csv  > log\base_s%%S.log 2>&1"
  @REM START "sync_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync                                             --sync-db out_test\db_sync_s%%S.pkl  --csv out_test\cond_sync_s%%S.csv  --diaglog out_test\diag_sync_s%%S.csv  > log\sync_s%%S.log 2>&1"
  @REM START "virz_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --viriale --zeta-vir                               --sync-db out_test\db_virz_s%%S.pkl  --csv out_test\cond_virz_s%%S.csv  --diaglog out_test\diag_virz_s%%S.csv  > log\virz_s%%S.log 2>&1"
  @REM START "pav_s%%S"   /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --pav-com                                          --sync-db out_test\db_pav_s%%S.pkl   --csv out_test\cond_pav_s%%S.csv   --diaglog out_test\diag_pav_s%%S.csv   > log\pav_s%%S.log 2>&1"
  START "tutto_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --viriale --zeta-vir --pav-com --chi-basc    --sync-db out_test\db_tutto_s%%S.pkl --csv out_test\cond_tutto_s%%S.csv --diaglog out_test\diag_tutto_s%%S.csv > log\tutto_s%%S.log 2>&1"
)

REM ================= VIDEO (camera fissa, seed 1 - NO db, i video non si spezzano) =========
@REM START "video_base_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7                                                 --out out_video\video_base_s1.mp4  > log\video_base_s1.log 2>&1"
@REM START "video_virz_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --viriale --zeta-vir                             --out out_video\video_virz_s1.mp4  > log\video_virz_s1.log 2>&1"
START "video_tutto_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --sync --viriale --zeta-vir --pav-com --chi-basc --out out_video\video_tutto_s1.mp4 > log\video_tutto_s1.log 2>&1"

echo Lanciati. Diaglog in out_test\, DB in out_test\db_*.pkl, video in out_video\, log in log\.
echo SPEZZARE: se si interrompe, RILANCIA questo stesso .bat -> riprende dal DB.
echo RIPARTIRE PULITO: cancella out_test\db_*.pkl (o aggiungi --db-cleanup ai comandi).