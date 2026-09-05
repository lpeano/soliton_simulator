@echo off
REM CAMPAGNA B=8 CON TRACKING DEL PICCO COSTRUTTIVO CORRETTO
REM OFF/ON seriale per seme; output separati dalla campagna precedente.
set SIM=soliton_simulator.py
set B=8
set NM=3
set SEP=16
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_tracking_spin_picco_scala8
if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === TRACKING PICCO SPIN: B=%B% sep=%SEP% passi=%PASSI% ===
for %%S in (1 2 3) do (
  echo [OFF] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\tracking_picco_scala8_off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [ON] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --spin-feedback --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\tracking_picco_scala8_on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna completata.
goto :fine
:errore
echo Errore nella campagna: controllare il log del seme corrente.
exit /b 1
:fine
pause
