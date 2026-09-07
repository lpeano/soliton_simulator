@echo off
REM ============================================================================
REM MATRICE CS-DINAMICO NELL'ORDINE RICHIESTO
REM
REM Ordine per ogni seme:
REM   FULL       -> FULL+CS
REM   CORE       -> CORE+CS
REM   FEEDBACK   -> FEEDBACK+CS
REM   BASE       -> BASE+CS
REM
REM B=1, sep=8, 2000 passi, 3 semi, seriale.
REM FULL    = spinore vivo + spin-feedback + chi-core
REM CORE    = spinore vivo + chi-core
REM FEEDBACK= spinore vivo + spin-feedback
REM BASE    = spinore vivo
REM +CS     = aggiunge --cs-dinamico
REM Output in cartella nuova: nessun DB vecchio viene riutilizzato.
REM ============================================================================
set SIM=soliton_simulator.py
set NM=3
set SEP=8
set PASSI=2000
set OGNI=10
set DBOGNI=100
if not exist log\matrice_cs_ordine mkdir log\matrice_cs_ordine

echo === MATRICE CS: FULL, CORE, FEEDBACK, BASE ===
echo === 3 semi, 8 bracci per seme, esecuzione seriale ===

for %%S in (1 2 3) do (
  echo [FULL] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_full_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_full_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_full_s%%S.csv > log\matrice_cs_ordine\matrice_cs_full_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [FULL+CS] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_fullcs_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_fullcs_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_fullcs_s%%S.csv > log\matrice_cs_ordine\matrice_cs_fullcs_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [CORE] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_core_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_core_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_core_s%%S.csv > log\matrice_cs_ordine\matrice_cs_core_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [CORE+CS] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_corecs_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_corecs_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_corecs_s%%S.csv > log\matrice_cs_ordine\matrice_cs_corecs_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [FEEDBACK] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_feedback_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_feedback_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_feedback_s%%S.csv > log\matrice_cs_ordine\matrice_cs_feedback_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [FEEDBACK+CS] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --spin-feedback --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_feedbackcs_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_feedbackcs_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_feedbackcs_s%%S.csv > log\matrice_cs_ordine\matrice_cs_feedbackcs_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [BASE] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_base_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_base_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_base_s%%S.csv > log\matrice_cs_ordine\matrice_cs_base_s%%S.log 2>&1
  if errorlevel 1 goto :errore
  echo [BASE+CS] seed %%S
  python %SIM% --batch --nmasse %NM% --sep %SEP% --seed %%S --passi %PASSI% --ogni %OGNI% --verlet --sync --spinore-vivo --chi-core --cs-dinamico --sync-db db\matrice_cs_ordine\db_basecs_s%%S.pkl --db-ogni %DBOGNI% --csv csv\matrice_cs_ordine\cond_basecs_s%%S.csv --diaglog csv\matrice_cs_ordine\diag_basecs_s%%S.csv > log\matrice_cs_ordine\matrice_cs_basecs_s%%S.log 2>&1
  if errorlevel 1 goto :errore
)

echo Campagna completata.
goto :fine

:errore
echo Errore: controllare il log del braccio corrente.
exit /b 1

:fine
pause
