@echo off
REM ============================================================================
REM REGIMI a 2000 passi (guscio-morbido ON): sep 5/6/8/12, 1 seme.
REM Oltre la formazione: dove coer_01 cala davvero? le masse restano 2?
REM Predizione (fallita a 400 passi): sep grande -> coer_01 ~0 (fuori portata).
REM ============================================================================
set SIM=soliton_simulator.py
set PASSI=2000
set OGNI=10
set OUT=out_guscio_regimi
set CHAIN=--sync --cs-dinamico --verlet --spinore-vivo --spin-feedback --chi-core --viriale --zeta-vir --pav-com --chi-basc --polo-maturo --olon-part --ls-azim --verso-chi --tau-d0 --zeta-loc --plast-din --calore-vett --guscio-morbido
if not exist log\guscio_regimi mkdir log\guscio_regimi

echo === REGIMI 2000 passi (guscio-morbido ON): sep 5/6/8/12, seed 1 ===
for %%P in (5 6 8 12) do (
  echo [sep %%P]
  python %SIM% --batch --nmasse 2 --sep %%P --seed 1 --passi %PASSI% --ogni %OGNI% %CHAIN% --sync-db db\guscio_regimi\db_sep%%P.pkl --db-ogni 200 --csv csv\guscio_regimi\cond_sep%%P.csv --diaglog csv\guscio_regimi\diag_sep%%P.csv > log\guscio_regimi\guscio_regimi_sep%%P.log 2>&1
  if errorlevel 1 goto :errore
)
echo REGIMI completati.
goto :fine

:errore
echo ERRORE, vedi log\guscio_regimi\guscio_regimi_sep*.log
:fine
