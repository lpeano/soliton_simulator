@echo off
REM ============================================================================
REM A/B --tw-spinore: aggancio della torsione a 4pi (doppia copertura) allo spinore.
REM OFF vs ON, sep 6, 2000 passi, 3 semi. Catena completa invariata; solo il flag cambia.
REM Domanda: il verso dello spinore PERSISTE (spin_cluster_omega resta alto, NON si
REM auto-spegne con l'ordine) o muore come SPIN_LARMOR? Controllo: corr(S_M, omega).
REM Output/DB DISTINTI (off/on) per seme.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=2
set SEP=6
set PASSI=2000
set OGNI=10
set DBOGNI=200
set CHAIN=--sync --cs-dinamico --verlet --spinore-vivo --spin-feedback --chi-core --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --ls-azim --verso-chi --tau-d0 --zeta-loc --plast-din --calore-vett
if not exist log\tw_spinore mkdir log\tw_spinore
REM db\<campagna>\ e csv\<campagna>\ le crea il motore (auto-mkdir). log\<campagna>\ serve al redirect di shell.

echo === A/B TW-SPINORE: sep=%SEP%, passi=%PASSI%, 3 semi (ON poi OFF) ===
for %%S in (1 2 3) do (
  echo [ON seed %%S]
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CHAIN% --tw-spinore --sync-db db\tw_spinore\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv csv\tw_spinore\cond_on_s%%S.csv --diaglog csv\tw_spinore\diag_on_s%%S.csv > log\tw_spinore\on_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
for %%S in (1 2 3) do (
  echo [OFF seed %%S]
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CHAIN% --sync-db db\tw_spinore\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv csv\tw_spinore\cond_off_s%%S.csv --diaglog csv\tw_spinore\diag_off_s%%S.csv > log\tw_spinore\off_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna tw-spinore completata.
goto :fine

:errore
echo ERRORE, vedi log\tw_spinore\*.log
:fine
