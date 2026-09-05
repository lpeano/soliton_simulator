@echo off
REM ============================================================================
REM CAMPAGNA ESPLORATIVA B=8 DEL FEEDBACK SPINORIALE
REM
REM Non e' una prova definitiva della fisica nativa: --scala 8 modifica la
REM descrizione efficace. La separazione e' portata a sep=16 per mantenere
REM sep/lambda uguale al riferimento nativo sep=8, dato lambda_8=1.6.
REM
REM Esecuzione seriale appaiata:
REM   seed 1 OFF -> seed 1 ON -> seed 2 OFF -> seed 2 ON -> seed 3 OFF -> seed 3 ON
REM ============================================================================
set SIM=soliton_simulator.py
set B=8
set NM=3
set SEP=16
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_spin_feedback_scala8_esplorativo

if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === CAMPAGNA ESPLORATIVA: B=%B%, sep=%SEP%, passi=%PASSI% ===
echo === ordine seriale OFF/ON per seme ===
echo.

for %%S in (1 2 3) do (
  echo [OFF] B=%B% seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\spinfb_scala8_exp_off_s%%S.log 2>&1
  if errorlevel 1 echo ERRORE OFF seed %%S & goto :errore

  echo [ON] B=%B% seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --spin-feedback --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\spinfb_scala8_exp_on_s%%S.log 2>&1
  if errorlevel 1 echo ERRORE ON seed %%S & goto :errore
)

echo.
echo Campagna esplorativa completata in %OUT%\.
goto :fine

:errore
echo Campagna interrotta: controllare il log corrispondente.
exit /b 1

:fine
pause
