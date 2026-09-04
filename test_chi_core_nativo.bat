@echo off
REM ============================================================================
REM A/B FISICO: CHIRALITA' EMERGENTE DEL CORE LOCALE
REM
REM OFF: dinamica attuale, nessun uso della chiralita' del core nel frame-dragging.
REM ON : --chi-core, il segno emerge da rho0/rhoc e dalla maschera radiale locale.
REM Nessun selettore chi=+1 e nessun --spin-feedback: una sola modifica fisica.
REM Scala nativa B=1, 3 semi, esecuzione seriale.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_chi_core_nativo
if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === A/B CHI-CORE: B=1, sep=%SEP%, passi=%PASSI% ===
for %%S in (1 2 3) do (
  echo [OFF] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\chicore_off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [ON] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\chicore_on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna chi-core completata.
goto :fine
:errore
echo Errore: controllare il log del seme corrente.
exit /b 1
:fine
pause
