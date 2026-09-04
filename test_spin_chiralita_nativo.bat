@echo off
REM ============================================================================
REM CAMPAGNA NATIVA: SPIN E CHIRALITA' NELLO STESSO INTORNO DEL PICCO
REM
REM Le colonne m*_picco_spin_plus/minus, contrasto e Q sono diagnostiche e
REM vengono calcolate sempre dal codice aggiornato. OFF/ON differiscono solo
REM per il feedback spinoriale sugli archi.
REM IMPORTANTE: la misura principale m*_picco_* usa TUTTI i solitoni del
REM dominio del picco. Non usare --spin-positivi: quel filtro sarebbe imposto.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_spin_chiralita_nativo
if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === SPIN/CHIRALITA NATIVA: B=1, sep=%SEP%, passi=%PASSI% ===
for %%S in (1 2 3) do (
  echo [OFF] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --cs-dinamico --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\spinchi_nativo_off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [ON] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --cs-dinamico --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\spinchi_nativo_on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna completata.
goto :fine
:errore
echo Errore: controllare il log del seme corrente.
exit /b 1
:fine
pause
