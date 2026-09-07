@echo off
REM ============================================================================
REM FASE 1 - REGIMI (guscio-morbido ON): sep 5/6/8, 400 passi, 1 seme.
REM Scopo: le masse restano 2 (distinte) o fondono a 1? coer_01/Lz_orb_01 con ON
REM reagiscono (>~0) o ~0? -> identifica SEP_UTILE (masse=2 E coer_01 reagisce).
REM Predizione: sep 8 fuori portata (coer_01~0); sep 5-6 utile se masse=2.
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=400
set OGNI=10
set CHAIN=--sync --cs-dinamico --verlet --spinore-vivo --spin-feedback --chi-core --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --ls-azim --verso-chi --tau-d0 --zeta-loc --plast-din --calore-vett --guscio-morbido
if not exist log\guscio_fase1 mkdir log\guscio_fase1

echo === FASE 1 REGIMI (guscio-morbido ON): sep 5/6/8, 400 passi, seed 1 ===
for %%P in (5 6 8) do (
  echo [sep %%P]
  python %SIM% --batch --nmasse 2 --sep %%P --seed 1 --passi %PASSI% --ogni %OGNI% %CHAIN% --sync-db db\guscio_fase1\db_sep%%P.pkl --db-ogni 200 --csv csv\guscio_fase1\cond_sep%%P.csv --diaglog csv\guscio_fase1\diag_sep%%P.csv > log\guscio_fase1\guscio_fase1_sep%%P.log 2>&1
  if errorlevel 1 goto :errore
)
echo FASE 1 completata.
goto :fine

:errore
echo ERRORE, vedi log\guscio_fase1\guscio_fase1_sep*.log
:fine
