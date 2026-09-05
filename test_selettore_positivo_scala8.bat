@echo off
REM ============================================================================
REM TEST ESPLORATIVO DEL SELETTORE POSITIVO DELLO SPINORE DI GRUPPO
REM
REM --spin-positivi e' per ora SOLO DIAGNOSTICO: non modifica la dinamica.
REM Confronta, nella stessa massa e nello stesso run:
REM   m*_picco_*       = tutti i generatori
REM   m*_picco_pos_*   = soli generatori perc_chi=+1
REM
REM B=8, sep=16 mantiene sep/lambda uguale al riferimento B=1, sep=8.
REM Esecuzione seriale su tre semi.
REM ============================================================================
set SIM=soliton_simulator.py
set B=8
set NM=3
set SEP=16
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_selettore_positivo_scala8

if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === SELETTORE POSITIVO: B=%B%, sep=%SEP%, passi=%PASSI% ===
echo === soli generatori perc_chi=+1 nella misura per-picco ===
echo.

for %%S in (1 2 3) do (
  echo [SEME %%S]
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --spin-positivi --sync-db %OUT%\db_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_s%%S.csv --diaglog %OUT%\diag_s%%S.csv > log\selettore_pos_scala8_s%%S.log 2>&1
  if errorlevel 1 echo ERRORE seme %%S & goto :errore
)

echo.
echo Test selettore positivo completato in %OUT%\.
goto :fine

:errore
echo Test interrotto: controllare il log del seme corrente.
exit /b 1

:fine
pause
