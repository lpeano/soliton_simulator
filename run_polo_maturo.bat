@echo off
REM ============================================================================
REM  TEST: il POLO MATURO da' precessione? (strategia 3 - la piu' promettente)
REM  Il polo maturo rompe il bilanciamento dei +-pi (olonomia netta ~0.52,
REM  coerente e concorde - verificato). DOMANDA: quel verso coerente e'
REM  AZIMUTALE (precessione, Lz_orb accumula) o RADIALE (coerente ma non ruota)?
REM  Confronto: --chi-basc (sorgente bilanciata) vs --chi-basc --polo-maturo.
REM  Spezzabile col DB. Un seme alla volta.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set DBOGNI=100
set SEMI=1

if not exist out_pm mkdir out_pm
if not exist log     mkdir log

echo === POLO MATURO (seme %SEMI%, %PASSI% passi) ===
echo.

for %%S in (%SEMI%) do (
  START "base_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc               --sync-db out_pm\db_base_s%%S.pkl --db-ogni %DBOGNI% --csv out_pm\cond_base_s%%S.csv --diaglog out_pm\diag_base_s%%S.csv > log\base_s%%S.log 2>&1"
  START "polo_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --polo-maturo --sync-db out_pm\db_polo_s%%S.pkl --db-ogni %DBOGNI% --csv out_pm\cond_polo_s%%S.csv --diaglog out_pm\diag_polo_s%%S.csv > log\polo_s%%S.log 2>&1"
)

echo Lanciati. Al ritorno: Lz_orb accumula con --polo-maturo (precessione) o resta rumore (radiale)?
echo Altri semi: SEMI=1 -> 2 -> 3.
