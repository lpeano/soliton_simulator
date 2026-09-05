@echo off
REM ============================================================================
REM CAMPAGNA SERIALE A SCALA NATIVA DEL FEEDBACK SPINORIALE
REM
REM Nessun coarse-graining: B=1 (nessun --scala).
REM OFF e ON sono eseguiti uno alla volta, per seme:
REM   seed 1 OFF -> seed 1 ON -> seed 2 OFF -> seed 2 ON -> seed 3 OFF -> seed 3 ON
REM
REM Il feedback e' l'unica differenza tra le braccia. Spinore vivo attivo in entrambe.
REM Output separati per non sovrascrivere la campagna coarse-grained precedente.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_spin_feedback_nativo

if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === CAMPAGNA NATIVA SERIALE: B=1, passi=%PASSI%, semi 1 2 3 ===
echo === ordine: OFF e ON appaiati per ogni seme ===
echo.

for %%S in (1 2 3) do (
  echo [OFF] scala nativa seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\spinfb_nativo_off_s%%S.log 2>&1
  if errorlevel 1 echo ERRORE OFF seed %%S & goto :errore

  echo [ON]  scala nativa seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\spinfb_nativo_on_s%%S.log 2>&1
  if errorlevel 1 echo ERRORE ON seed %%S & goto :errore
)

echo.
echo Campagna nativa completata: 6 run seriali in %OUT%\.
echo Osservabile diretta: spin_feedback_arco nel diaglog.
goto :fine

:errore
echo Campagna interrotta per errore. Controllare il log corrispondente.
exit /b 1

:fine
pause
