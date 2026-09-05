@echo off
REM ============================================================================
REM TODO PRIORITARIO 1 (Checkpoint 2026-09-04): SPIN DEL NUCLEO + INERZIA GUSCIO
REM
REM Misura spin_core / spin_core_disp sulla MASCHERA DEL NUCLEO (senza selezione
REM perc_chi) e, in piu', le metriche di congelamento da guscio:
REM   m0_Mdyn, m0_Mcoh, m0_Rinerzia, m0_Jrot, m0_Jshell_frac, m0_Ncore, m0_Nshell.
REM Catena fisica completa del Checkpoint. 2000 passi, 3 semi, seriale.
REM Verifica attesa: se il guscio (Nshell, Jshell_frac, Rinerzia) cresce, la
REM precessione (m0_Lz) e lo spin del nucleo (m0_spin_core) calano -> congelamento.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=2
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_spincore
REM --diag-lente-ogni 50: throttla solo chi_core (lenta/costante); le VELOCI (Lz, Berry, Neel, spin_core) restano a ogni passo (niente aliasing).
set CHAIN=--sync --cs-dinamico --verlet --spinore-vivo --spin-feedback --chi-core --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --ls-azim --verso-chi --tau-d0 --zeta-loc --plast-din --calore-vett --diag-lente-ogni 50
if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === SPIN_CORE + INERZIA GUSCIO: B=1, sep=%SEP%, passi=%PASSI%, 3 semi ===
for %%S in (1 2 3) do (
  echo [seed %%S]
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% %CHAIN% --sync-db %OUT%\db_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_s%%S.csv --diaglog %OUT%\diag_s%%S.csv > log\spincore_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)
echo Campagna spin_core completata.
goto :fine

:errore
echo ERRORE nel run, vedi log\spincore_s*.log
:fine
