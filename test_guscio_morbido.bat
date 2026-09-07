@echo off
REM ============================================================================
REM FASE 2 - A/B DIFFUSIONE DI SUPERFICIE (--guscio-morbido)
REM
REM Confronto OFF vs ON a parita' di tutto il resto (catena completa + cs-dinamico).
REM Attesa: con ON il BORDO si smussa (guscio_idx e contrasto d0 calano), il NUCLEO
REM resta rigido, e (premio) la coerenza/correlazione di spin fra masse vicine sale.
REM Output/DB SEPARATI da out_spincore (gira in parallelo senza collidere).
REM 2 masse, sep 8, 2000 passi, 2 semi, seriale.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=2
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set CHAIN=--sync --cs-dinamico --verlet --spinore-vivo --spin-feedback --chi-core --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --ls-azim --verso-chi --tau-d0 --zeta-loc --plast-din --calore-vett
if not exist log\guscio_morbido mkdir log\guscio_morbido

echo === GUSCIO MORBIDO A/B: B=1, sep=%SEP%, passi=%PASSI%, 2 semi ===
for %%S in (1 2) do (
  echo [OFF seed %%S]
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CHAIN% --sync-db db\guscio_morbido\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\guscio_morbido\cond_off_s%%S.csv --diaglog csv\guscio_morbido\diag_off_s%%S.csv > log\guscio_morbido\guscio_off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [ON seed %%S]
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CHAIN% --guscio-morbido --sync-db db\guscio_morbido\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\guscio_morbido\cond_on_s%%S.csv --diaglog csv\guscio_morbido\diag_on_s%%S.csv > log\guscio_morbido\guscio_on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna guscio-morbido completata.
goto :fine

:errore
echo ERRORE nel run, vedi log\guscio_morbido\guscio_*.log
:fine
