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
if not exist log\chi_core_nativo mkdir log\chi_core_nativo

echo === A/B CHI-CORE: B=1, sep=%SEP%, passi=%PASSI% ===
for %%S in (1 2 3) do (
  echo [OFF] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --sync-db db\chi_core_nativo\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\chi_core_nativo\cond_off_s%%S.csv --diaglog csv\chi_core_nativo\diag_off_s%%S.csv > log\chi_core_nativo\chicore_off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [ON] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --sync-db db\chi_core_nativo\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\chi_core_nativo\cond_on_s%%S.csv --diaglog csv\chi_core_nativo\diag_on_s%%S.csv > log\chi_core_nativo\chicore_on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna chi-core completata.
goto :fine
:errore
echo Errore: controllare il log del seme corrente.
exit /b 1
:fine
pause
