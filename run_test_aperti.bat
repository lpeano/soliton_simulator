@echo off
REM ============================================================================
REM  TEST APERTI con DB (idempotente+versionato) — 3 masse, run lungo
REM  Attivo: solo TUTTO. DB per seme, salvataggio ogni 100 passi (--db-ogni 100).
REM  SPEZZARE: se si interrompe, RILANCIA questo stesso .bat -> riprende dal DB.
REM  RIPARTIRE PULITO: cancella out_test\db_*.pkl (o aggiungi --db-cleanup).
REM  NB: DB rifiutato se cambi il codice (hash diverso) -> allora --db-cleanup.
REM  NB2: la FISICA riprende identica; il tracking-masse riparte (colonne m0_/dist_
REM       potrebbero rietichettare le masse dopo un resume).
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set FRAMES=20000
set FPS=24
set OGNI=5
set DBOGNI=25
set SEMI=1 2 3

if not exist out_test  mkdir out_test
if not exist out_video mkdir out_video
if not exist log        mkdir log

echo === TEST APERTI con DB (%NM% masse, %PASSI% passi, semi %SEMI%) ===
echo     solo TUTTO attivo, DB per seme ogni %DBOGNI% passi (spezzabile)
echo.

REM ================= BATCH (con DB per seme) =================
for %%S in (%SEMI%) do (
  @REM START "base_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI%                                                    --sync-db out_test\db_base_s%%S.pkl  --db-ogni %DBOGNI% --csv out_test\cond_base_s%%S.csv  --diaglog out_test\diag_base_s%%S.csv  > log\base_s%%S.log 2>&1"
  @REM START "sync_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync                                             --sync-db out_test\db_sync_s%%S.pkl  --db-ogni %DBOGNI% --csv out_test\cond_sync_s%%S.csv  --diaglog out_test\diag_sync_s%%S.csv  > log\sync_s%%S.log 2>&1"
  @REM START "virz_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --viriale --zeta-vir                               --sync-db out_test\db_virz_s%%S.pkl  --db-ogni %DBOGNI% --csv out_test\cond_virz_s%%S.csv  --diaglog out_test\diag_virz_s%%S.csv  > log\virz_s%%S.log 2>&1"
  @REM START "pav_s%%S"   /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --pav-com                                          --sync-db out_test\db_pav_s%%S.pkl   --db-ogni %DBOGNI% --csv out_test\cond_pav_s%%S.csv   --diaglog out_test\diag_pav_s%%S.csv   > log\pav_s%%S.log 2>&1"
  START "tutto_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --viriale --zeta-vir --pav-com --chi-basc    --sync-db out_test\db_tutto_s%%S.pkl --db-ogni %DBOGNI% --csv out_test\cond_tutto_s%%S.csv --diaglog out_test\diag_tutto_s%%S.csv > log\tutto_s%%S.log 2>&1"
)

REM ================= VIDEO (camera fissa, seed 1 - i video non si spezzano) =========
@REM START "video_base_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7                                                 --out out_video\video_base_s1.mp4  > log\video_base_s1.log 2>&1"
@REM START "video_virz_s1"  /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --viriale --zeta-vir                             --out out_video\video_virz_s1.mp4  > log\video_virz_s1.log 2>&1"
START "video_tutto_s1" /MIN cmd /c "python %SIM% --test N-MASSE --nmasse %NM% --sep %SEP% --seed 1 --giri 0 --ppf 1 --frames %FRAMES% --fps %FPS% --size 0.7,0.7,0.7 --sync --viriale --zeta-vir --pav-com --chi-basc --out out_video\video_tutto_s1.mp4 > log\video_tutto_s1.log 2>&1"

echo Lanciati. Diaglog in out_test\, DB in out_test\db_*.pkl (ogni %DBOGNI% passi), log in log\.
echo SPEZZARE: se si interrompe, RILANCIA questo stesso .bat -> riprende dal DB.
echo RIPARTIRE PULITO: cancella out_test\db_*.pkl