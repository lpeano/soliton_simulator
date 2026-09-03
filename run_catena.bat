@echo off
REM ============================================================================
REM  TEST FINALE: la catena completa che i dubbi hanno costruito
REM   --chi-basc     : organizza le chiralita' (gradiente vecchio/nuovo)
REM   --polo-maturo  : verso COERENTE dal polo che matura (olonomia netta 0.52)
REM   --viriale      : converte radiale -> tangenziale
REM   --olon-part    : il verso coerente comanda la PARTIZIONE (non solo la direzione)
REM  DOMANDA: ora Lz_orb ACCUMULA (precessione) o resta rumore/radiale?
REM  Confronto progressivo per isolare cosa aggiunge ogni pezzo.
REM  Spezzabile col DB. Un seme alla volta.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set DBOGNI=100
set SEMI=1

if not exist out_cat mkdir out_cat
if not exist log      mkdir log

echo === CATENA POLO-MATURO + OLON-PART (seme %SEMI%, %PASSI% passi) ===
echo.

@REM for %%S in (%SEMI%) do (
@REM   START "vir_s%%S"   /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --chi-basc --viriale                            --sync-db out_cat\db_vir_s%%S.pkl  --db-ogni %DBOGNI% --csv out_cat\cond_vir_s%%S.csv  --diaglog out_cat\diag_vir_s%%S.csv  > log\vir_s%%S.log 2>&1"
@REM   START "polo_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --chi-basc --viriale --polo-maturo             --sync-db out_cat\db_polo_s%%S.pkl --db-ogni %DBOGNI% --csv out_cat\cond_polo_s%%S.csv --diaglog out_cat\diag_polo_s%%S.csv > log\polo_s%%S.log 2>&1"
@REM   START "full_s%%S"  /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --chi-basc --viriale --polo-maturo --olon-part --sync-db out_cat\db_full_s%%S.pkl --db-ogni %DBOGNI% --csv out_cat\cond_full_s%%S.csv --diaglog out_cat\diag_full_s%%S.csv > log\full_s%%S.log 2>&1"
@REM )
START "video_n_masse_3_fisse-sep-3.9" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 3.9 --seed 42 --passi %PASSI% --ogni %OGNI% --viriale --olon-part --polo-maturo --sync --calore-vett --sync-db out_cat\db_video_n_masse_3_fisse-sep-3.9.pkl --db-ogni %DBOGNI% --csv out_cat\cond_video_n_masse_3_fisse-sep-3.9.csv --diaglog out_cat\diag_video_n_masse_3_fisse-sep-3.9.csv > log\video_n_masse_3_fisse-sep-3.9.log 2>&1 "
START "video_n_masse_3_fisse-sep-7" /MIN cmd /c "python %SIM% --batch --nmasse 3 --sep 7 --seed 42 --passi %PASSI% --ogni %OGNI% --viriale --olon-part --polo-maturo --sync --calore-vett --sync-db out_cat\db_video_n_masse_3_fisse-sep-7.pkl --db-ogni %DBOGNI% --csv out_cat\cond_video_n_masse_3_fisse-sep-7.csv --diaglog out_cat\diag_video_n_masse_3_fisse-sep-7.csv > log\video_n_masse_3_fisse-sep-7.log 2>&1 "
echo Lanciati. Al ritorno: Lz_orb per vir / polo / full - accumula con olon-part?
echo Altri semi: SEMI=1 -> 2 -> 3.
