@echo off
REM ============================================================================
REM A/B VELOCITA' METRICA LOCALE
REM
REM OFF: CS_M=2.0 uniforme, percorso storico.
REM ON : --cs-dinamico, cs_eff(rho) con tanh e media armonica sugli archi.
REM
REM Il diaglog ON registra cs_eff_min/med/max. Il confronto usa stessa rete,
REM stesso seme, stesso integratore e stessi flag; i risultati sono separati.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_cs_dinamico
set SEMI=1 2 3

if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === CS DINAMICO A/B: B=1, sep=%SEP%, passi=%PASSI% ===
for %%S in (%SEMI%) do (
  echo [OFF] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\cs_dinamico_off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [ON] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --cs-dinamico --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\cs_dinamico_on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna CS dinamico completata.
goto :fine
:errore
echo Errore: controllare il log del seme corrente.
exit /b 1
:fine
pause
