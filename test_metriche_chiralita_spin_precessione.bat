@echo off
REM ============================================================================
REM CAMPAGNA COMPLETA: METRICHE DI CHIRALITA', SPIN E PRECESSIONE
REM
REM Tutte le braccia usano la massa completa nel dominio del picco: nessun
REM filtro chi=+1 costruisce lo spin principale.
REM
REM Bracci:
REM   BASE      spinore vivo, senza feedback e senza chi-core
REM   FEEDBACK  + feedback locale spinore->archi
REM   CORE      + chiralita' emergente del core nei canali collettivi
REM   FULL      + feedback + chiralita' emergente del core
REM
REM Misure nel diaglog:
REM   m*_picco_chi, m*_picco_spin, m*_picco_spin_{x,y,z}
REM   m*_picco_spin_plus/minus, m*_picco_contrasto, m*_picco_q_{x,y,z}, q_modulo
REM   m*_picco_verso_{x,y,z}, berry_spin_*, m*_Lz, Lz_orb_*, spin_feedback_arco
REM   chi_core_*, rho0_core_max, rho_c_core, r_core_medio
REM
REM Il test e' diagnostico/A-B: non promuove nessuna legge a default.
REM Esecuzione seriale per evitare contesa di risorse e mantenere i confronti
REM riproducibili. 3 semi x 4 bracci = 12 run.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
set OUT=out_metriche_chiralita_spin_precessione

if not exist %OUT% mkdir %OUT%
if not exist log mkdir log

echo === METRICHE CHIRALITA-SPIN-PRECESSIONE: B=1, sep=%SEP%, passi=%PASSI% ===
echo === 4 bracci x 3 semi, esecuzione seriale ===
echo.

for %%S in (1 2 3) do (
  echo [BASE] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db %OUT%\db_base_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_base_s%%S.csv --diaglog %OUT%\diag_base_s%%S.csv > log\metriche_base_s%%S.log 2>&1
  if errorlevel 1 goto :errore

  echo [FEEDBACK] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db %OUT%\db_feedback_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_feedback_s%%S.csv --diaglog %OUT%\diag_feedback_s%%S.csv > log\metriche_feedback_s%%S.log 2>&1
  if errorlevel 1 goto :errore

  echo [CORE] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db %OUT%\db_core_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_core_s%%S.csv --diaglog %OUT%\diag_core_s%%S.csv > log\metriche_core_s%%S.log 2>&1
  if errorlevel 1 goto :errore

  echo [FULL] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db %OUT%\db_full_s%%S.pkl --db-ogni %DBOGNI% --csv %OUT%\cond_full_s%%S.csv --diaglog %OUT%\diag_full_s%%S.csv > log\metriche_full_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)

echo.
echo Campagna completata: 12 run in %OUT%\.
echo Analizzare ultimo 50%% e stabilita' temporale, non solo l'ultima riga.
goto :fine

:errore
echo Campagna interrotta: controllare il log del braccio e del seme corrente.
exit /b 1

:fine
pause
