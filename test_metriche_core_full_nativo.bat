@echo off
REM ============================================================================
REM CAMPAGNA FOCALIZZATA: I DUE BRACCI PIU' NUOVI/INTERESSANTI
REM
REM CORE:  spinore vivo + chiralita' emergente del core
REM FULL:  CORE + feedback locale spinore->archi
REM
REM La massa principale usa tutti i nodi del dominio del picco.
REM S+/S-, contrasto e Q sono solo scomposizioni diagnostiche.
REM 3 semi, 2000 passi, esecuzione seriale.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
if not exist log\metriche_core_full_nativo mkdir log\metriche_core_full_nativo

echo === CORE vs FULL: B=1, sep=%SEP%, passi=%PASSI% ===
for %%S in (1 2 3) do (
  echo [CORE] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db db\metriche_core_full_nativo\db_core_s%%S.pkl --db-ogni %DBOGNI% --csv csv\metriche_core_full_nativo\cond_core_s%%S.csv --diaglog csv\metriche_core_full_nativo\diag_core_s%%S.csv > log\metriche_core_full_nativo\corefull_core_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [FULL] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db db\metriche_core_full_nativo\db_full_s%%S.pkl --db-ogni %DBOGNI% --csv csv\metriche_core_full_nativo\cond_full_s%%S.csv --diaglog csv\metriche_core_full_nativo\diag_full_s%%S.csv > log\metriche_core_full_nativo\corefull_full_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna CORE/FULL completata.
goto :fine
:errore
echo Errore: controllare il log corrente.
exit /b 1
:fine
pause
