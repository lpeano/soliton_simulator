@echo off
REM ============================================================================
REM SCREENING COARSE-GRAINED DEL FEEDBACK SPINORIALE SUGLI ARCHI
REM
REM Scopo: verificare se il feedback locale derivato da <psi_i|psi_j> produce
REM un segnale robusto quando il coarse-graining aumenta la scala efficace.
REM NON e' ancora la campagna finale del nastro di Moebius: --scala cambia la
REM rappresentazione della rete e serve solo come screening di fattibilita'.
REM
REM OFF e ON differiscono SOLO per --spin-feedback.
REM Entrambi usano --spinore-vivo, --sync e la stessa scala B.
REM Osservabili: feedback_arco_ampiezza_ultima, berry_spin_*, lift, olonomia.
REM Disciplina: 2000 passi, 3 semi. Se il segnale emerge, ripetere a scala 1
REM su almeno 2000 passi prima di interpretarlo fisicamente.
REM ============================================================================
set SIM=soliton_simulator.py
set B=8
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_spin_feedback_scala_v2

if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === SCREENING COARSE-GRAINED: B=%B%, passi=%PASSI%, semi 1 2 3 ===
echo === OFF/ON feedback spinoriale, spinore vivo in entrambe le braccia ===
echo.

for %%S in (1 2 3) do (
  echo [OFF] scala B=%B% seed %%S
  START "spinfb_scala_off_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --sync-db %OUT%\db_off_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_off_s%%S.csv --diaglog %OUT%\diag_off_s%%S.csv > log\spinfb_scala_off_s%%S.log 2>&1"
  echo [ON]  scala B=%B% seed %%S
  START "spinfb_scala_on_s%%S" /MIN cmd /c "python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --scala %B% --verlet --sync --spinore-vivo --spin-feedback --sync-db %OUT%\db_on_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_on_s%%S.csv --diaglog %OUT%\diag_on_s%%S.csv > log\spinfb_scala_on_s%%S.log 2>&1"
)

echo.
echo Screening lanciato: 6 run in %OUT%\, log in log\.
echo Confrontare OFF/ON su feedback_arco_ampiezza_ultima, berry_spin_* e olonomia.
echo Un segnale ON non dimostra il Moebius: richiede conferma a scala 1 e run lunghi.
pause
