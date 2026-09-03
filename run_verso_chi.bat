@echo off
REM ============================================================================
REM  TEST: l'AGGANCIO AL VERSO STABILE ferma l'inversione? (precessione?)
REM  FRAME_DRAG pilotato dal verso CHIRALE stabile (--verso-chi) invece del tw
REM  oscillante. Con --chi-basc (organizza le chiralita' in gradiente vecchio/nuovo).
REM  Confronto: senza vs con --verso-chi.
REM  DOMANDA: Lz_orb smette di invertirsi (coerenza del verso ~1) e accumula?
REM    SI -> l'aggancio al verso stabile da' precessione (il ponte mancante)
REM    NO -> il verso chirale e' azimutalmente simmetrico, non basta
REM  Un seme alla volta (memoria): SEMI=1, poi 2, poi 3.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=16
set PASSI=20000
set OGNI=5
set DBOGNI=100
set SEMI=1

if not exist out_vc mkdir out_vc
if not exist log     mkdir log

echo === AGGANCIO VERSO STABILE (seme %SEMI%, %PASSI% passi) ===
echo.

for %%S in (%SEMI%) do (
  START "senza_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc            --sync-db out_vc\db_senza_s%%S.pkl --db-ogni %DBOGNI% --csv out_vc\cond_senza_s%%S.csv --diaglog out_vc\diag_senza_s%%S.csv > log\senza_s%%S.log 2>&1"
  START "con_s%%S"   /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --sync --chi-basc --verso-chi --sync-db out_vc\db_con_s%%S.pkl   --db-ogni %DBOGNI% --csv out_vc\cond_con_s%%S.csv   --diaglog out_vc\diag_con_s%%S.csv   > log\con_s%%S.log 2>&1"
)

echo Lanciati. Al ritorno: Lz_orb coerenza del verso, senza vs con --verso-chi.
echo Spezzabile col DB. Altri semi: cambia SEMI=1 in 2, poi 3.
