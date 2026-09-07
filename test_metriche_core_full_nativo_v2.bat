@echo off
REM Campagna pulita CORE/FULL con codice corrente. B=1, sep=8, 3 semi.
REM CORE = spinore vivo + chi-core; FULL = CORE + spin-feedback.
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
if not exist log\metriche_core_full_nativo_v2 mkdir log\metriche_core_full_nativo_v2

echo === CORE/FULL V2: B=1, sep=%SEP%, passi=%PASSI% ===
for %%S in (1 2 3) do (
  echo [CORE] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db db\metriche_core_full_nativo_v2\db_core_s%%S.pkl --db-ogni %DBOGNI% --csv csv\metriche_core_full_nativo_v2\cond_core_s%%S.csv --diaglog csv\metriche_core_full_nativo_v2\diag_core_s%%S.csv > log\metriche_core_full_nativo_v2\corefull_v2_core_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [FULL] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db db\metriche_core_full_nativo_v2\db_full_s%%S.pkl --db-ogni %DBOGNI% --csv csv\metriche_core_full_nativo_v2\cond_full_s%%S.csv --diaglog csv\metriche_core_full_nativo_v2\diag_full_s%%S.csv > log\metriche_core_full_nativo_v2\corefull_v2_full_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna CORE/FULL V2 completata.
goto :fine
:errore
echo Errore: controllare il log corrente.
exit /b 1
:fine
pause
